from DataBase import db
from HandDirection import HandDirection
from HandModel import HandModel
from hand import Hand
from Util import dict_to_json, json_to_dict




db.connect()
db.create_tables([HandModel])

# TEMPORARILY CREATE HAND FOR TESTING --- START
hand = Hand()

hand.rawPositions = {
    0: [0.1, 0.2, 0.3],
    1: [0.4, 0.5, 0.6]
}

hand.pairWiseDistances = {
    (0, 1): 0.42,
    (0, 2): 0.51,
    (1, 2): 0.18
}

hand.pairWiseAngles = {
    (0, 1): 35.2,
    (0, 2): 71.8
}

hand.handFactor = 0.85
hand.handThreshold = 0.5
hand.handDirection = HandDirection.LEFT

# TEMPORARILY CREATE HAND FOR TESTING --- END

stored_hand = HandModel.create(
    rawPositions=hand.rawPositions,
    pairWiseDistances=dict_to_json(hand.pairWiseDistances),
    pairWiseAngles=dict_to_json(hand.pairWiseAngles),
    handDirection=hand.handDirection.value,
    handFactor=hand.handFactor,
    handThreshold=hand.handThreshold
)

print(f"Stored hand with ID: {stored_hand.id}")
stored_hand = HandModel.get_by_id(stored_hand.id)

