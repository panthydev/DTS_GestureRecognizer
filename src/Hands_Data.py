from hand import Hand
import HandDirection
from CalculateHands import Calculate_Hands as CalHands

class HandsData:
    def __init__(self):
        RightHand = Hand()
        LeftHand = Hand()
        self.HandsDictionary : dict[str, Hand] = {"Right" : RightHand, "Left" : LeftHand}

    def UpdateDirections(self, DetectionResults):
        for i in range(len(DetectionResults.handedness)):

            handDirection = DetectionResults.handedness[i][0].display_name
            
            self.HandsDictionary[handDirection].handDirection = handDirection 

            self.HandsDictionary[handDirection].rawPositions = DetectionResults.hand_landmarks[i]

            self.HandsDictionary[handDirection].handFactor = DetectionResults.handedness[i][0].score

            self.CalculateHands(handDirection)

    def CalculateHands(self, handDirection):
        self.HandsDictionary[handDirection].pairWiseDistances = CalHands.CalulateDistance(
        CalHands, self.HandsDictionary[handDirection].rawPositions, handDirection)

        self.HandsDictionary[handDirection].pairWiseAngles = CalHands.CalulateAngle(
        CalHands, self.HandsDictionary[handDirection].rawPositions, handDirection)