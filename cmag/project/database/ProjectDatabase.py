from pathlib import Path

from .BaseModel      import CMagDatabaseProxy
from .ChallengeModel import CMagChallengeModel
from .FileModel      import CMagFileModel

from peewee import (
    SqliteDatabase,
    DatabaseProxy,
    Model, ForeignKeyField,
    CharField, IntegerField
)

class CMagProjectDatabase:

    Challenge = CMagChallengeModel
    File      = CMagFileModel

    def __init__(self, path: Path):
        self._database = SqliteDatabase(path)
        CMagDatabaseProxy.initialize(self._database)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    @property
    def o(self): return self._database

    def open(self):
        self._database.connect()

    def close(self):
        self._database.close()
