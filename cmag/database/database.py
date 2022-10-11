from peewee import SqliteDatabase
from .base_model import CMagBaseModel, CMagDatabaseProxy

class CMagDatabase:
    
    def __init__(self, path: str):
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