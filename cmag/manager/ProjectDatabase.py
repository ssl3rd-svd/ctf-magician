from pathlib import Path

from peewee import (
    SqliteDatabase,
    DatabaseProxy,
    Model, ForeignKeyField,
    CharField, IntegerField
)

CMagProjDatabaseProxy = DatabaseProxy()

class BaseModel(Model):
    class Meta:
        database = CMagProjDatabaseProxy

class CMagProjChallenge(BaseModel):
    id       = CharField(unique=True)
    name     = CharField()
    desc     = CharField()
    category = IntegerField()

class CMagProjFile(BaseModel):
    id        = IntegerField(primary_key=True, unique=True)
    challenge = ForeignKeyField(CMagProjChallenge, backref="files")
    filepath  = CharField(unique=True)

class CMagProjectDatabase:

    Challenge = CMagProjChallenge
    File      = CMagProjFile

    def __init__(self, path: Path):
        self._database = SqliteDatabase(path)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
        return self

    @property
    def database(self): return self._database

    def open(self):
        CMagProjDatabaseProxy.initialize(self._database)

    def close(self):
        self._database.close()

