import pickletools

from peewee import Model, FloatField, TextField, JSONField


from DataBase import db


class HandModel(Model):

    name = TextField()
    pairWiseDistances = JSONField()
    pairWiseAngles = JSONField()
    pairWiseDistanceWeights = JSONField()
    pairWiseAngleWeights = JSONField()

    class Meta:
        database = db
        table_name = 'hands'