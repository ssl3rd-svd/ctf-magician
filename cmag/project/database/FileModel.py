from peewee import IntegerField, ForeignKeyField, CharField
from .BaseModel import CMagBaseModel
from .ChallengeModel import CMagChallengeModel

class CMagFileModel(CMagBaseModel):
    id        = IntegerField(primary_key=True, unique=True)
    challenge = ForeignKeyField(CMagChallengeModel, backref="files")
    filepath  = CharField(unique=True)