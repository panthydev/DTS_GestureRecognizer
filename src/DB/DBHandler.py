from DataBase import db
from HandDirection import HandDirection
from HandModel import HandModel
from hand import Hand
from Util import dict_to_json, json_to_dict

class DBHandler:
    def __init__(self):
        db.connect()
        db.create_tables([HandModel])


    def SaveHand(self, hand):
        HandModel.create(
            rawPositions=dict_to_json(hand.rawPositions),
            pairWiseDistances=dict_to_json(hand.pairWiseDistances),
            pairWiseAngles=dict_to_json(hand.pairWiseAngles),
            HandDirection=hand.HandDirection.value,
            handFactor=hand.HandFactor,
            handThreshold=hand.HandThreshold,
        )

    def GetHandById(self,id):
        stored = HandModel.get_by_id(id)

        hand = Hand()

        hand.rawPositions = json_to_dict(stored.rawPositions)
        hand.pairWiseDistances = json_to_dict(stored.pairWiseDistances)
        hand.pairWiseAngles = json_to_dict(stored.pairWiseAngles)

        hand.handDirection = HandDirection(stored.handDirection)
        hand.handFactor = stored.handFactor
        hand.handThreshold = stored.handThreshold

        return hand


    

