from HandDirection import HandDirection


class Hand:

    """ This object represents a hand and has all the info for it, like the individual points, distances, etc.

    """

    rawPositions = {}
    pairWiseDistances = {}
    pairWiseAngles = {}
    handDirection = HandDirection.UNDEFINED
    handFactor = 0.0  # left or right handedness probability, from 0 -> 1
    handThreshold = 0.0
    def __init__(self):
        pass

