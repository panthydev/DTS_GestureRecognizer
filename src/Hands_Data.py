from hand import Hand
import HandDirection
from CalculateHands import Calculate_Hands as CalHands

class HandsData:
    def __init__(self):
        self.name = ""
        RightHand : Hand = Hand()
        LeftHand : Hand = Hand()
        self.HandsDictionary : dict[str, Hand] = {"Right" : RightHand, "Left" : LeftHand}

        self.rawPositions : dict[int, float] = {}

        self.pairWiseDistances : dict[tuple[int, int], float] = {}
        self.pairWiseAngles : dict[tuple[int, int], float] = {}
        self.pairWiseDistanceWeights : dict[tuple[int, int], float] = {}
        self.pairWiseAngleWeights : dict[tuple[int, int], float] = {}

    def UpdateHandObjects(self, DetectionResults):
        self.FillHandsRawInfo(DetectionResults)
        self.MergeHands()
        self.CalculateHandGeometry()

    def FillHandsRawInfo(self, DetectionResults):
        for i in range(len(DetectionResults.handedness)):
            handDirection = DetectionResults.handedness[i][0].display_name
            
            self.HandsDictionary[handDirection].handDirection = handDirection 

            self.HandsDictionary[handDirection].rawPositions = DetectionResults.hand_landmarks[i]

            self.HandsDictionary[handDirection].handFactor = DetectionResults.handedness[i][0].score

    def MergeHands(self):
        h = 0
        for hand in self.HandsDictionary:
            for pos in range(len(self.HandsDictionary[hand].rawPositions)):
                self.rawPositions[h] = self.HandsDictionary[hand].rawPositions[pos]
                h += 1

    def CalculateHandGeometry(self):
        """Calculates pairwise distances and angles for both hands"""
        self.pairWiseDistances = CalHands.CalulateDistance(CalHands, self.rawPositions)
        self.pairWiseAngles = CalHands.CalulateAngle(CalHands, self.rawPositions)

        self.pairWiseDistanceWeights = CalHands.AssignWeightAngles(CalHands, 42)
        self.pairWiseAngleWeights = CalHands.AssignWeightDistance(CalHands, 42)
