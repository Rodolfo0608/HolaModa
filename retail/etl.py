"""Carga completa validada. Uso: python -m retail.etl --file ruta.csv"""
import argparse
import csv
import hashlib
import io
import logging
import math
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from time import perf_counter

from retail.db import DEFAULT_DB, SCHEMA, connect

log = logging.getLogger(__name__)
TEXT_FIELDS = {
    'Gender': 'gender', 'Item Purchased': 'item', 'Category': 'category',
    'Location': 'location', 'Size': 'size', 'Color': 'color', 'Season': 'season',
    'Payment Method': 'payment', 'Shipping Type': 'shipping',
    'Preferred Payment Method': 'preferred_payment', 'Frequency of Purchases': 'frequency',
}
REQUIRED = set(TEXT_FIELDS) | {
    'Customer ID', 'Age', 'Purchase Amount (USD)', 'Review Rating',
    'Subscription Status', 'Discount Applied', 'Promo Code Used', 'Previous Purchases',
}


def transform(row):
    result = {}
    for source, target in TEXT_FIELDS.items():
        value = (row[source] or '').strip()
        if not value or len(value) > 120:
            raise ValueError(f'Campo vacío o demasiado largo: {source}')
        result[target] = value
    for source, target, minimum, maximum in [
        ('Customer ID', 'customer_id', 1, 2**31-1),
        ('Age', 'age', 0, 120),
        ('Previous Purchases', 'previous_purchases', 0, 2**31-1),
    ]:
        value = int(row[source])
        if not minimum <= value <= maximum:
            raise ValueError(f'Valor fuera de rango: {source}')
        result[target] = value
    # Los importes se almacenan en centavos para evitar errores de coma flotante.
    amount = Decimal(row['Purchase Amount (USD)'])
    if not amount.is_finite() or amount < 0 or amount > 100000000:
        raise ValueError('Importe fuera de rango')
    cents = amount * 100
    if cents != cents.to_integral_value():
        raise ValueError('El importe admite como máximo dos decimales')
    result['amount_cents'] = int(cents)
    rating = float(row['Review Rating'])
    if not math.isfinite(rating) or not 0 <= rating <= 5:
        raise ValueError('Calificación fuera de rango')
    result['rating'] = rating
    for source, target in [('Subscription Status', 'subscribed'),
                           ('Discount Applied', 'discounted'), ('Promo Code Used', 'promo')]:
        value = (row[source] or '').strip().lower()
        if value not in ('yes', 'no'):
            raise ValueError(f'Se esperaba Yes o No: {source}')
        result[target] = int(value == 'yes')
    return result


def load(file_path, db_path=DEFAULT_DB):
    started = perf_counter()
    source = Path(file_path)
    content = source.read_bytes()
    reader = csv.DictReader(io.StringIO(content.decode('utf-8-sig')))
    missing = REQUIRED - set(reader.fieldnames or [])
    if missing:
        raise ValueError('Faltan columnas: ' + ', '.join(sorted(missing)))
    records, seen = [], set()
    for line, row in enumerate(reader, start=2):
        try:
            record = transform(row)
            if record['customer_id'] in seen:
                raise ValueError('Customer ID duplicado en la muestra')
            seen.add(record['customer_id'])
            records.append(record)
        except (ValueError, TypeError, InvalidOperation) as error:
            raise ValueError(f'Fila {line}: {error}') from error
    if not records:
        raise ValueError('El archivo no contiene registros')
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    fingerprint = hashlib.sha256(content).hexdigest()
    with connect(db_path) as db:
        db.executescript(SCHEMA)
        # La validación termina antes de reemplazar la muestra. El commit es único.
        with db:
            db.execute('DELETE FROM purchases')
            columns = list(records[0])
            query = f"INSERT INTO purchases ({','.join(columns)}) VALUES ({','.join(':'+c for c in columns)})"
            db.executemany(query, records)
            db.execute('INSERT INTO etl_runs(loaded_at,source_name,sha256,row_count,duration_ms) VALUES(?,?,?,?,?)',
                       (datetime.now(timezone.utc).isoformat(), source.name, fingerprint,
                        len(records), round((perf_counter()-started)*1000)))
    log.info('Carga confirmada: filas=%s sha256=%s', len(records), fingerprint)
    return {'rows': len(records), 'sha256': fingerprint}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', default='data/raw/shopping_trends.csv')
    parser.add_argument('--db', default=str(DEFAULT_DB))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    try:
        load(args.file, args.db)
    except (OSError, ValueError) as error:
        log.error('No se completó la carga: %s', error)
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
