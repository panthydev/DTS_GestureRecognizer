from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark


from HandDirection import HandDirection


class Hand:

    """ This object represents a hand and has all of the info for it, like the individual points, distances, etc.

    """



    rawPositions : dict[tuple[int, int], NormalizedLandmark] = {}
    pairWiseDistances : dict[tuple[int, int], float] = {}
    pairWiseAngles : dict[tuple[int, int], float] = {}
    handDirection : HandDirection = HandDirection.UNDEFINED
    handFactor : float # left or right handedness probablity, from 0 -> 1
    handThreshold  : float


    def __init__(self):
        pass
