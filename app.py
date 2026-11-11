import logging
import os
import sqlite3
import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from retail.db import DEFAULT_DB, connect

FILTERS = {'category': 'category', 'season': 'season', 'gender': 'gender', 'discounted': 'discounted'}
GROUPS = {'category': 'category', 'season': 'season', 'item': 'item', 'payment': 'payment'}


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(DATABASE=os.environ.get('DATABASE_PATH', str(DEFAULT_DB)), MAX_CONTENT_LENGTH=1048576)
    if config:
        app.config.update(config)

    def where(paginated=False):
        allowed = set(FILTERS) | ({'page', 'per_page'} if paginated else set())
        if set(request.args) - allowed:
            raise ValueError('Parámetro desconocido')
        clauses, values = [], []
        for key, column in FILTERS.items():
            if len(request.args.getlist(key)) > 1:
                raise ValueError(f'Parámetro repetido: {key}')
            value = request.args.get(key, '')
            if not value:
                continue
            if len(value) > 120 or (key == 'discounted' and value not in ('0', '1')):
                raise ValueError(f'Filtro inválido: {key}')
            clauses.append(f'{column} = ?')
            values.append(value)
        return (' WHERE ' + ' AND '.join(clauses) if clauses else ''), values

    def query(sql, values=()):
        if not Path(app.config['DATABASE']).is_file():
            raise sqlite3.OperationalError('Base pendiente de carga')
        with connect(app.config['DATABASE']) as db:
            return [dict(row) for row in db.execute(sql, values).fetchall()]

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'same-origin'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'"
        response.headers['Cache-Control'] = 'no-store'
        return response

    @app.errorhandler(ValueError)
    def invalid(error):
        return jsonify(error={'code': 'invalid_request', 'message': str(error)}), 400

    @app.errorhandler(sqlite3.Error)
    def unavailable(error):
        app.logger.exception('No se pudo consultar SQLite')
        return jsonify(error={'code': 'data_unavailable', 'message': 'Datos no disponibles. Ejecuta el ETL y revisa el registro del servidor.'}), 503

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error={'code': error.name, 'message': error.description}), error.code

    @app.errorhandler(Exception)
    def unexpected(error):
        reference = uuid.uuid4().hex[:12]
        app.logger.exception('Error interno referencia=%s', reference)
        return jsonify(error={'code': 'internal_error', 'message': 'Error interno', 'reference': reference}), 500

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.get('/docs')
    def docs():
        return render_template('docs.html')

    @app.get('/api/health')
    def health():
        count = query('SELECT COUNT(*) AS rows FROM purchases')[0]['rows']
        if count == 0:
            return jsonify(status='empty', rows=0), 503
        return jsonify(status='ok', rows=count)

    @app.get('/api/filters')
    def filters():
        return jsonify({key: [r['value'] for r in query(f'SELECT DISTINCT {key} AS value FROM purchases ORDER BY {key}')]
                        for key in ('category', 'season', 'gender')})

    @app.get('/api/summary')
    def summary():
        clause, values = where()
        row = query('SELECT COUNT(*) AS records, COUNT(DISTINCT customer_id) AS customers, '
                    'COALESCE(SUM(amount_cents),0) AS total_cents, AVG(amount_cents) AS average_cents, '
                    'AVG(rating) AS average_rating, SUM(discounted) AS discounted_records FROM purchases' + clause, values)[0]
        return jsonify(records=row['records'], customers=row['customers'],
                       total_amount_usd=row['total_cents']/100,
                       average_amount_usd=round(row['average_cents']/100, 2) if row['records'] else None,
                       average_rating=round(row['average_rating'], 2) if row['records'] else None,
                       discounted_records=row['discounted_records'] or 0)

    @app.get('/api/groups/<dimension>')
    def groups(dimension):
        if dimension not in GROUPS:
            raise ValueError('Agrupación permitida: category, season, item o payment')
        clause, values = where()
        column = GROUPS[dimension]
        # Solo los nombres de columnas de esta lista controlada entran en el SQL.
        rows = query(f'SELECT {column} AS label, COUNT(*) AS records, '
                     f'SUM(amount_cents)/100.0 AS amount_usd FROM purchases{clause} '
                     f'GROUP BY {column} ORDER BY amount_usd DESC, label ASC', values)
        return jsonify(dimension=dimension, data=rows)

    @app.get('/api/purchases')
    def purchases():
        clause, values = where(paginated=True)
        for name in ('page', 'per_page'):
            if len(request.args.getlist(name)) > 1:
                raise ValueError(f'Parámetro repetido: {name}')
        page = int(request.args.get('page', '1'))
        per_page = int(request.args.get('per_page', '10'))
        if not 1 <= page <= 1000000 or not 1 <= per_page <= 100:
            raise ValueError('page debe estar entre 1 y 1000000 y per_page entre 1 y 100')
        total = query('SELECT COUNT(*) AS total FROM purchases' + clause, values)[0]['total']
        rows = query('SELECT customer_id, age, gender, item, category, amount_cents/100.0 AS amount_usd, '
                     'season, discounted, rating FROM purchases' + clause + ' ORDER BY customer_id LIMIT ? OFFSET ?',
                     values + [per_page, (page-1)*per_page])
        return jsonify(data=rows, page=page, per_page=per_page, total=total,
                       pages=(total+per_page-1)//per_page)

    @app.get('/api/pipeline')
    def pipeline():
        rows = query('SELECT * FROM etl_runs ORDER BY id DESC LIMIT 1')
        return jsonify(latest_run=rows[0] if rows else None)

    @app.get('/api/openapi.json')
    def openapi():
        from retail.openapi import specification
        return jsonify(specification())

    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    create_app().run(host='127.0.0.1', port=5000, debug=False)
