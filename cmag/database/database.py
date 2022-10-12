from peewee import SqliteDatabase
from .base_model import CMagBaseModel, CMagDatabaseProxy
from .exceptions import *

class CMagDatabase:

    def exception_handler(self, e):
        # TODO:
        pass

    @ExceptionDecorator(CMagDatabaseFailed, exception_handler)
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

    @ExceptionDecorator(CMagDatabaseOpenError, exception_handler)
    def open(self):
        self.database.connect()

    @ExceptionDecorator(CMagDatabaseCloseError, exception_handler)
    def close(self):
        self.database.close()