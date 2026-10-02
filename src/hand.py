from HandDirection import HandDirection


class Hand:

    """ This object represents a hand and has all of the info for it, like the individual points, distances, etc.

    """


    def __init__(self, detectionResult):
        j = 0
        self.rawPositions = {}
        self.pairWiseDistances = {}
        self.pairWiseAngles = {}
        self.handDirection = HandDirection.UNDEFINED
        self.handFactor = 0.0 # left or right handedness probablity, from 0 -> 1
        self.handThreshold = 0.0

        for landmarkPosition in detectionResult.hand_landmarks[0]:
            self.rawPositions[j] = landmarkPosition
            j += 1
        pass
        
