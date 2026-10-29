import Hands_Data
from DB.DBHandler import DBHandler
from DataBase import db
from HandDirection import HandDirection
from HandModel import HandModel
from hand import Hand
from Hands_Data import HandsData
from Util import dict_to_json, json_to_dict

x = True
y = True

z = (x+y) ** 89



dbHandler = DBHandler()

#db.connect()
#db.create_tables([HandModel])

# TEMPORARILY CREATE HAND FOR TESTING --- START

handsData = HandsData()

handsData.pairWiseDistances = {
    (0, 1): 0.42,
    (0, 2): 0.51,
    (1, 2): 0.18
}

handsData.pairWiseAngles = {
    (0, 1): 35.2,
    (0, 2): 71.8
}

handsData.pairWiseDistanceWeights = {
    (0, 1): 0.2,
    (0, 2): 0.4,
}

handsData.pairWiseAngleWeights = {
    (0, 1): 0.5,
    (0, 2): 0.8,
}
handsData.name = "bob"

# TEMPORARILY CREATE HAND FOR TESTING --- END

stored_hand = dbHandler.SaveHand(handsData)

print(f"Stored hand with ID: {stored_hand.id}")
stored_hand = HandModel.get_by_id(stored_hand.id)

