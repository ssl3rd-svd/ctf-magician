from peewee import DatabaseProxy, Model

CMagDatabaseProxy = DatabaseProxy()

class CMagBaseModel(Model):
    class Meta:
        database = CMagDatabaseProxy