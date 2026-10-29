from DataBase import db
from HandDirection import HandDirection
from HandModel import HandModel
from Hands_Data import HandsData
from hand import Hand
from Util import dict_to_json, json_to_dict

class DBHandler:
    def __init__(self):
        db.connect()
        db.create_tables([HandModel])


    def SaveHand(self, handsData : HandsData):
        savedHand = HandModel.create(
            pairWiseDistances=dict_to_json(handsData.pairWiseDistances),
            pairWiseAngles=dict_to_json(handsData.pairWiseAngles),
            pairWiseDistanceWeights=dict_to_json(handsData.pairWiseAngleWeights),
            pairWiseAngleWeights=dict_to_json(handsData.pairWiseAngleWeights),
            name=str(handsData.name)
        )
        return savedHand

    def GetHandById(self,id):
        stored = HandModel.get_by_id(id)

        handData = HandsData()


        handData.pairWiseDistances = json_to_dict(stored.pairWiseDistances)
        handData.pairWiseAngles = json_to_dict(stored.pairWiseAngles)
        handData.pairWiseDistanceWeights = json_to_dict(stored.pairWiseDistanceWeights)
        handData.pairWiseAngleWeights = json_to_dict(stored.pairWiseAngleWeights)

        return handData


    

