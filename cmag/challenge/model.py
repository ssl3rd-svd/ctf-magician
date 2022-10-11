from peewee import CharField, IntegerField
from cmag.database.base_model import CMagBaseModel

class CMagChallengeModel(CMagBaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    desc = CharField(null=True)
