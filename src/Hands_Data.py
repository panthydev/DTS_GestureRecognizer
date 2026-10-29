from hand import Hand
import HandDirection
from CalculateHands import Calculate_Hands as CalHands

class HandsData:
    def __init__(self):
        self.name = ""
        RightHand = Hand()
        LeftHand = Hand()
        self.HandsDictionary : dict[str, Hand] = {"Right" : RightHand, "Left" : LeftHand}

        self.rawPositions : dict[int, float] = {}

        self.pairWiseDistances : dict[tuple[int, int], float] = {}
        self.pairWiseAngles : dict[tuple[int, int], float] = {}
        self.pairWiseDistanceWeights : dict[tuple[int, int], float] = {}
        self.pairWiseAngleWeights : dict[tuple[int, int], float] = {}

    def UpdateDirections(self, DetectionResults):
        for i in range(len(DetectionResults.handedness)):

            handDirection = DetectionResults.handedness[i][0].display_name
            
            self.HandsDictionary[handDirection].handDirection = handDirection 

            self.HandsDictionary[handDirection].rawPositions = DetectionResults.hand_landmarks[i]

            self.HandsDictionary[handDirection].handFactor = DetectionResults.handedness[i][0].score

        h = 0
        for hand in self.HandsDictionary:
            for pos in range(len(self.HandsDictionary[hand].rawPositions)):
                self.rawPositions[h] = self.HandsDictionary[hand].rawPositions[pos]
                h += 1

        self.CalculateHands()

    def CalculateHands(self):
        #self.HandsDictionary[handDirection].pairWiseDistances = CalHands.CalulateDistance(
        #CalHands, self.HandsDictionary[handDirection].rawPositions, handDirection)
        #self.HandsDictionary[handDirection].pairWiseAngles = CalHands.CalulateAngle(
        #CalHands, self.HandsDictionary[handDirection].rawPositions, handDirection)
        self.pairWiseDistances = CalHands.CalulateDistance(CalHands, self.rawPositions)
        self.pairWiseAngles = CalHands.CalulateAngle(CalHands, self.rawPositions)