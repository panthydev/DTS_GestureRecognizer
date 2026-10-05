from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark


from HandDirection import HandDirection


class Hand:

    """ This object represents a hand and has all of the info for it, like the individual points, distances, etc.

    """


    def __init__(self, detectionResult):
        j = 0
        self.rawPositions : dict[tuple[int, int], NormalizedLandmark] = {}
        self.pairWiseDistances : dict[tuple[int, int], float] = {}
        self.pairWiseAngles : dict[tuple[int, int], float] = {}
        self.handDirection : HandDirection = HandDirection.UNDEFINED
        self.handFactor : float # left or right handedness probablity, from 0 -> 1
        self.handThreshold  : float

        for landmarkPosition in detectionResult.hand_landmarks[0]:
            self.rawPositions[j] = landmarkPosition
            j += 1
        pass

