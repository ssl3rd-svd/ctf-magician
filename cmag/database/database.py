from peewee import SqliteDatabase
from pathlib import Path
from .base_model import CMagDatabaseProxy

class CMagDatabase:

    def __init__(self, path: str):
        if Path(path).is_dir():
            raise IsADirectoryError
        self._database = SqliteDatabase(path)
        CMagDatabaseProxy.initialize(self._database)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    @property
    def database(self): return self._database

    def open(self):
        self.database.connect()

    def close(self):
        self.database.close()