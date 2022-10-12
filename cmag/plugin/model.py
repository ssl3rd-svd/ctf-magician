from peewee import CharField, IntegerField, ForeignKeyField, BooleanField
from cmag.database.base_model import CMagBaseModel

class CMagPluginModel(CMagBaseModel):
    id = IntegerField(primary_key=True)
    callname = CharField(unique=True)
    impfrom = CharField(unique=True)
    options = CharField()
    enabled = BooleanField()
