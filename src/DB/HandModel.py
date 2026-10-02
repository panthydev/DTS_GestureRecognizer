import pickletools

from peewee import Model, FloatField, TextField, JSONField


from DataBase import db


class HandModel(Model):

    rawPositions = JSONField()
    pairWiseDistances = JSONField()
    pairWiseAngles = JSONField()

    handDirection = JSONField()

    handFactor = FloatField()
    handThreshold = FloatField()

    class Meta:
        database = db
        table_name = 'hands'