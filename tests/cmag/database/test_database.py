import pytest
from peewee import *

from cmag.database import CMagDatabase
from cmag.database.base_model import CMagBaseModel
from cmag.database.exceptions import CMagDatabaseFailed

@pytest.fixture
def db_path(tmp_path):
    db_path = tmp_path / 'database.db'
    return db_path

@pytest.fixture
def cmag_db(db_path):
    return CMagDatabase(db_path)

class CMagTestModel(CMagBaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)

class Test00CMagDatabaseInit:

    def test00_init(self, db_path):
        cmag_db = CMagDatabase(db_path)
        assert isinstance(cmag_db, CMagDatabase)
        assert isinstance(cmag_db.database, SqliteDatabase)
        with cmag_db.database as database:
            CMagTestModel.create_table()
        assert db_path.exists() is True

    def test00_init_not_file_path(self, tmp_path):
        assert tmp_path.is_dir() is True
        with pytest.raises(Exception) as CMagDatabaseFailed:
            cmag_db = CMagDatabase(tmp_path)

    def test00_init_doubly_open(self, cmag_db):
        cmag_db.open()

    def test00_init_doubly_close(self, db_path):
        cmag_db = CMagDatabase(db_path)
        cmag_db.close()
        cmag_db.close()

# almost like peewee test...
class Test01CMagDatabaseCRUD:
    def test01_crud_simple_crud(self, cmag_db):
        with cmag_db.database as database:
            CMagTestModel.create_table()
            CMagTestModel.create(name='foo').save()
            CMagTestModel.create(name='bar').save()

            assert CMagTestModel.get(id=1).id == 1
            assert CMagTestModel.get(id=1).name == 'foo'
            assert CMagTestModel.get(id=2).id == 2
            assert CMagTestModel.get(id=2).name == 'bar'

            CMagTestModel.get(id=1).update(name='baz')
            CMagTestModel.get(id=2).delete()

    def test01_crud_doubly_create(self, cmag_db):
        with cmag_db.database as database:
            CMagTestModel.create_table()
            CMagTestModel.create(name="foo").save()
            with pytest.raises(IntegrityError):
                CMagTestModel.create(name="foo")

    def test01_crud_read_dosent_exist(self, cmag_db):
        with cmag_db.database as database:
            CMagTestModel.create_table()
            with pytest.raises(Exception):
                CMagTestModel.get(id=1)

    def test01_curd_doubly_delete(self, cmag_db):
        with cmag_db.database as database:
            CMagTestModel.create_table()
            CMagTestModel.create(name="foo").save()
            CMagTestModel.get(id=1).delete()
            CMagTestModel.get(id=1).delete()
