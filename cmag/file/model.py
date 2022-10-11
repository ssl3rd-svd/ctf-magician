from peewee import CharField, IntegerField, ForeignKeyField
from cmag.database.base_model import CMagBaseModel
from cmag.challenge.model import CMagChallengeModel

class CMagFileModel(CMagBaseModel):
    id = IntegerField(primary_key=True)
    root = IntegerField()
    type = IntegerField()
    path = CharField(unique=True)
    challenge = ForeignKeyField(CMagChallengeModel, backref="files")