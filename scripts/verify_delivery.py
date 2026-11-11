"""Coteja la fuente con SQLite y con el servidor local, sin modificar los datos."""
import argparse
import csv
import hashlib
import json
import math
import sqlite3
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]


def verify(base_url):
    source = ROOT / 'data/raw/shopping_trends.csv'
    raw = source.read_bytes()
    with source.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    total_cents = sum(int(Decimal(r['Purchase Amount (USD)'])*100) for r in rows)
    findings = []

    def check(condition, description):
        if not condition:
            raise AssertionError(description)
        findings.append(description)

    def get(path, expected=200):
        try:
            with urllib.request.urlopen(base_url+path, timeout=10) as response:
                code, body = response.status, response.read()
        except urllib.error.HTTPError as error:
            code, body = error.code, error.read()
        if code != expected:
            raise AssertionError(f'{path}: se esperaba {expected}, se recibió {code}')
        return json.loads(body)

    fingerprint = hashlib.sha256(raw).hexdigest()
    metadata = json.loads((ROOT/'data/source.json').read_text(encoding='utf-8'))
    check(fingerprint == metadata['sha256'], 'CSV coincide con el SHA-256 documentado')
    database_uri = (ROOT/'instance/retail.db').as_uri() + '?mode=ro'
    with sqlite3.connect(database_uri, uri=True) as db:
        stored = dict(db.execute('SELECT customer_id, amount_cents FROM purchases'))
        audit_hash = db.execute('SELECT sha256 FROM etl_runs ORDER BY id DESC LIMIT 1').fetchone()[0]
    expected_records = {int(r['Customer ID']):int(Decimal(r['Purchase Amount (USD)'])*100) for r in rows}
    check(len(expected_records) == len(rows), 'Identificadores únicos en la fuente completa')
    check(stored == expected_records, 'Todos los clientes e importes de SQLite coinciden con el CSV')
    check(audit_hash == fingerprint, 'Auditoría de SQLite identifica la fuente actual')
    check(get('/api/health')['rows'] == len(rows), 'Health informa la cantidad real de filas')
    summary = get('/api/summary')
    check(summary['records'] == len(rows), 'API de resumen coincide con el número de registros del CSV')
    check(Decimal(str(summary['total_amount_usd'])) == Decimal(total_cents)/100,
          'Monto acumulado de la API coincide con la suma independiente del CSV')
    check(summary['average_amount_usd'] == round(total_cents/len(rows)/100, 2), 'Compra promedio conciliada')
    check(summary['average_rating'] == round(statistics.mean(float(r['Review Rating']) for r in rows), 2),
          'Calificación promedio conciliada')

    for dimension, source_column in [('category','Category'), ('season','Season'),
                                     ('item','Item Purchased'), ('payment','Payment Method')]:
        grouped = defaultdict(lambda: {'records':0, 'cents':0})
        for row in rows:
            grouped[row[source_column]]['records'] += 1
            grouped[row[source_column]]['cents'] += int(Decimal(row['Purchase Amount (USD)'])*100)
        actual = get('/api/groups/'+dimension)['data']
        check(len(actual) == len(grouped) and all(
            r['records'] == grouped[r['label']]['records'] and
            Decimal(str(r['amount_usd'])) == Decimal(grouped[r['label']]['cents'])/100 for r in actual),
            f'Agrupación {dimension} conciliada con el CSV')

    for category in sorted({r['Category'] for r in rows}):
        for season in sorted({r['Season'] for r in rows}):
            subset = [r for r in rows if r['Category']==category and r['Season']==season]
            values = get('/api/summary?'+urllib.parse.urlencode({'category':category,'season':season}))
            amount = sum(Decimal(r['Purchase Amount (USD)']) for r in subset)
            check(values['records']==len(subset) and Decimal(str(values['total_amount_usd']))==amount,
                  f'Filtro combinado {category} / {season}: cantidad y monto conciliados')

    filters = get('/api/filters')
    check(filters['category']==sorted({r['Category'] for r in rows}), 'Categorías de filtro coinciden con la fuente')
    first = get('/api/purchases?per_page=10&page=1')
    second = get('/api/purchases?per_page=10&page=2')
    check(first['total']==len(rows) and len(first['data'])==10 and
          not ({r['customer_id'] for r in first['data']} & {r['customer_id'] for r in second['data']}),
          'Detalle paginado sin solapamiento en las dos primeras páginas')
    check(get('/api/summary?category=NoExiste')['average_amount_usd'] is None,
          'Selección vacía devuelve promedios nulos')
    check(get('/api/purchases?per_page=101',400)['error']['code']=='invalid_request',
          'Parámetro fuera de rango devuelve 400 controlado')
    check(get('/api/pipeline')['latest_run']['sha256']==fingerprint, 'API del pipeline publica la huella correcta')
    contract = get('/api/openapi.json')
    check(contract['openapi']=='3.0.3' and '/api/purchases' in contract['paths'], 'Contrato OpenAPI disponible por HTTP')
    for path in ['/', '/docs', '/static/app.css', '/static/app.js', '/static/vendor/chart.umd.js',
                 '/static/vendor/swagger-ui-bundle.js', '/static/vendor/swagger-ui.css']:
        with urllib.request.urlopen(base_url+path, timeout=10) as response:
            check(response.status==200 and len(response.read())>0, f'Recurso web disponible: {path}')

    timings = {}
    for path in ['/api/summary','/api/groups/category','/api/purchases?per_page=10']:
        samples = []
        for _ in range(10):
            start = perf_counter()
            get(path)
            samples.append((perf_counter()-start)*1000)
        timings[path] = {'requests':len(samples), 'median_ms':round(statistics.median(samples),2),
                         'p95_ms':round(sorted(samples)[math.ceil(len(samples)*0.95)-1],2)}
    return {'checked_at_panama':datetime.now(timezone(timedelta(hours=-5))).isoformat(),
            'scope':'Ejecución nativa local. No es una prueba de carga ni una auditoría de seguridad.',
            'python':sys.version.split()[0], 'rows':len(rows), 'total_usd':str(Decimal(total_cents)/100),
            'checks_passed':len(findings), 'checks':findings, 'http_sequential_timings':timings}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',default='http://127.0.0.1:5000')
    parser.add_argument('--output',default='docs/RESULTADO_COTEJO.json')
    args = parser.parse_args()
    try:
        report = verify(args.base_url.rstrip('/'))
    except (AssertionError, OSError, ValueError, sqlite3.Error) as error:
        parser.exit(1, f'No se completó el cotejo: {error}\nComprueba el servidor, el puerto, el CSV y la base antes de repetirlo.\n')
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"Cotejo aprobado: {report['checks_passed']} comprobaciones; {report['rows']} registros; USD {report['total_usd']}")
    print(json.dumps(report['http_sequential_timings'],ensure_ascii=False,indent=2))
