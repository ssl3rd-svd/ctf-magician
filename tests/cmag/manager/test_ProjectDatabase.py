import pytest

from cmag.manager import CMagProjectDatabase

@pytest.fixture
def dbpath(workdir):
    from secrets import token_hex
    from pathlib import Path
    dbpath = Path(workdir) / (token_hex(32) + '.db')
    return dbpath

def test01_dbinit(dbpath):
    database = CMagProjectDatabase(dbpath)
    database.open()
    database.close()

def test02_db_with_as(dbpath):
    with CMagProjectDatabase(dbpath) as db:
        db.Challenge.create_table()
        db.File.create_table()
