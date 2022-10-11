from peewee import CharField, IntegerField, ForeignKeyField, BooleanField
from cmag.database.base_model import CMagBaseModel

class CMagPluginModel(CMagBaseModel):
    id = IntegerField(primary_key=True)
    impfrom = CharField()
    options = CharField()
    enabled = BooleanField()
    
