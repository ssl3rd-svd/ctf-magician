from peewee import CharField, IntegerField
from .BaseModel import CMagBaseModel

class CMagChallengeModel(CMagBaseModel):
    id   = CharField(unique=True)
    name = CharField()
    desc = CharField(null=True)
