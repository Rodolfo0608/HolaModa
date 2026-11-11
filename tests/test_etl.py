import pytest

from retail.db import connect
from retail.etl import load, transform


def test_exact_money_and_normalization(sample_rows):
    sample_rows[0]['Category'] = ' Clothing '
    result = transform(sample_rows[0])
    assert result['amount_cents'] == 1010
    assert result['category'] == 'Clothing'
    assert result['subscribed'] == 1
    assert result['promo'] == 0


def test_reload_replaces_snapshot_without_duplicates(database, write_csv, sample_rows):
    load(write_csv(sample_rows[:2]), database)
    with connect(database) as db:
        assert db.execute('SELECT COUNT(*) FROM purchases').fetchone()[0] == 2
        assert db.execute('SELECT SUM(amount_cents) FROM purchases').fetchone()[0] == 3030
        assert db.execute('SELECT COUNT(*) FROM etl_runs').fetchone()[0] == 2


@pytest.mark.parametrize('field,value', [
    ('Age','-1'), ('Age','121'), ('Purchase Amount (USD)','-1'),
    ('Purchase Amount (USD)','nan'), ('Purchase Amount (USD)','1.001'),
    ('Review Rating','nan'), ('Review Rating','6'), ('Discount Applied','maybe'),
    ('Customer ID','0'), ('Previous Purchases','-1'), ('Category',' '),
])
def test_invalid_batch_preserves_previous_load(database, write_csv, sample_rows, field, value):
    sample_rows[1][field] = value
    with pytest.raises(ValueError, match='Fila 3'):
        load(write_csv(sample_rows), database)
    with connect(database) as db:
        assert db.execute('SELECT COUNT(*) FROM purchases').fetchone()[0] == 3
        assert db.execute('SELECT SUM(amount_cents) FROM purchases').fetchone()[0] == 6060
        assert db.execute('SELECT COUNT(*) FROM etl_runs').fetchone()[0] == 1


def test_duplicate_id_rejected(database, write_csv, sample_rows):
    sample_rows[1]['Customer ID'] = '1'
    with pytest.raises(ValueError, match='duplicado'):
        load(write_csv(sample_rows), database)


def test_missing_headers_and_empty_file(tmp_path, write_csv):
    path = tmp_path / 'invalid.csv'
    path.write_text('wrong\n1\n')
    with pytest.raises(ValueError, match='Faltan columnas'):
        load(path, tmp_path / 'new.db')
    with pytest.raises(ValueError, match='no contiene registros'):
        load(write_csv([]), tmp_path / 'new.db')
    assert not (tmp_path / 'new.db').exists()
