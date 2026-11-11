import sqlite3

import pytest

from retail.db import connect
from retail.etl import load


def test_write_failure_rolls_back_snapshot_and_audit(database, sample_rows, write_csv):
    # Simulamos una falla al insertar después del DELETE dentro de la transacción.
    with connect(database) as db:
        db.execute("CREATE TRIGGER fail_write BEFORE INSERT ON purchases BEGIN SELECT RAISE(ABORT, 'write failure'); END")
        db.commit()
    with pytest.raises(sqlite3.IntegrityError):
        load(write_csv(sample_rows[:1]), database)
    with connect(database) as db:
        assert db.execute('SELECT COUNT(*) FROM purchases').fetchone()[0] == 3
        assert db.execute('SELECT SUM(amount_cents) FROM purchases').fetchone()[0] == 6060
        assert db.execute('SELECT COUNT(*) FROM etl_runs').fetchone()[0] == 1
