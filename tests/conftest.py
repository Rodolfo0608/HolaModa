import csv

import pytest

from app import create_app
from retail.etl import REQUIRED, load


@pytest.fixture
def sample_rows():
    base = {field: 'Example' for field in REQUIRED}
    base.update({'Customer ID':'1','Age':'30','Purchase Amount (USD)':'10.10','Review Rating':'4.5',
                 'Subscription Status':'Yes','Discount Applied':'Yes','Promo Code Used':'No',
                 'Previous Purchases':'2','Category':'Clothing','Season':'Winter','Gender':'Female'})
    second = {**base,'Customer ID':'2','Purchase Amount (USD)':'20.20','Category':'Footwear','Discount Applied':'No'}
    third = {**base,'Customer ID':'3','Purchase Amount (USD)':'30.30','Season':'Summer','Gender':'Male'}
    return [base, second, third]


@pytest.fixture
def write_csv(tmp_path):
    def write(rows, fields=None):
        path = tmp_path / 'sample.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields or sorted(REQUIRED))
            writer.writeheader()
            writer.writerows(rows)
        return path
    return write


@pytest.fixture
def database(tmp_path, write_csv, sample_rows):
    path = tmp_path / 'sample.db'
    load(write_csv(sample_rows), path)
    return path


@pytest.fixture
def client(database):
    return create_app({'TESTING': True, 'DATABASE': str(database)}).test_client()
