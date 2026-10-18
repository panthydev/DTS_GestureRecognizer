from typing import List

import Hands_Data
import hand
from hand import Hand
from Hands_Data import HandsData

DistanceTolerance = 0.1
AngleTolerance = 0.1

# !!!!!!! READ THIS !!!!!!!
# currently the file is double the size it should be, ive just copied and pasted the whole thing, and made 2 version, for the issues mentioned below
#the top code is for single hand gesture examples, the code below is for the real deal, multi hand gestures



# should actually return key to gesture in DB that matches or the match directly
# currently returns the score of the comparison where 1 is a perfect match and 0 is the worst match possible lmao
# this currently doesn't take into account multi hand gestures, it assumes a gesture is always just one hand
# perhaps we should change gesture calculation to always be dual hand based...
# like perhaps we have a dictionary in Hands_Data with both hand mushed together
# so we have fx pairwise distances between point 2 and 32 (a point on left hand to the right hand)
# in any case, it doesnt change these calculations much, just needs a little adjustment.
# like we literally just switch out the dictionary we are enumerating on, its like 4 seconds of work
def CompareHandToGestureHand(CurrentHand : Hand, DBHand : Hand) -> float:

    SumOfDistanceWeightedSimilarties = 0
    SumOfDistanceWeights = 0


    #PairDistance is the key
    for PairDistance in CurrentHand.pairWiseDistances:

        weight = DBHand.pairWiseDistanceWeights[PairDistance]
        CurrentDistance = CurrentHand.pairWiseDistances[PairDistance]
        IdealDistance = DBHand.pairWiseDistances[PairDistance]


        #calculate difference
        difference = abs(CurrentDistance - IdealDistance)

        #calc similarity, will never be negative
        similarity = max(0, 1 - difference / DistanceTolerance)


        SumOfDistanceWeightedSimilarties += weight

        weightedSimilarity = similarity * weight

        SumOfDistanceWeightedSimilarties += weightedSimilarity

    finalDistanceScore = SumOfDistanceWeightedSimilarties / SumOfDistanceWeights

    SumOfAngleWeightedSimilarties = 0
    SumOfAngleWeights = 0

    for PairAngles in CurrentHand.pairWiseAngles:
        weight = DBHand.pairWiseAngleWeights[PairAngles]
        CurrentDistance = CurrentHand.pairWiseAngles[PairAngles]
        IdealDistance = DBHand.pairWiseAngles[PairAngles]

        # calculate difference
        difference = abs(CurrentDistance - IdealDistance)

        # calc similarity, will never be negative
        similarity = max(0, 1 - difference / AngleTolerance)

        SumOfAngleWeightedSimilarties += weight

        weightedSimilarity = similarity * weight

        SumOfAngleWeightedSimilarties += weightedSimilarity

    finalAngleScore = SumOfAngleWeightedSimilarties / SumOfAngleWeights


    finalScore = (finalDistanceScore + finalAngleScore) / 2 # we can modify this later and weigh angle or distance more if needed

    return finalScore


#returns a tuple that has the gesture that "won" and its score
#this function is lowkey expecting a list of handsData, so whoever makes the database stuff needs to make sure thats an option
def CompareHandToAllGestures(CurrentHand : HandsData, AllHands : List[HandsData]) -> tuple[float, Hand] :

    FinalScoresDict = {} # idk type hints arent working, its a [float, Hands_Data] dictionary

    for HandsDataObj in AllHands:
        #run comparison to gesture and add to the final dictionary
        Score =  CompareGestureToDBGesture(CurrentHand, HandsDataObj)
        FinalScoresDict[HandsDataObj] = Score

    closestMatch = (max(FinalScoresDict), FinalScoresDict[max(FinalScoresDict)])
    return closestMatch





#this is the exact same as earlier but takes a handsData object instead, performs the same calc tho
def CompareGestureToDBGesture(CurrentHand : HandsData, DBHand : HandsData) -> float:

    SumOfDistanceWeightedSimilarties = 0
    SumOfDistanceWeights = 0


    #PairDistance is the key
    for PairDistance in CurrentHand.pairWiseDistances:

        weight = DBHand.pairWiseDistanceWeights[PairDistance]
        CurrentDistance = CurrentHand.pairWiseDistances[PairDistance]
        IdealDistance = DBHand.pairWiseDistances[PairDistance]


        #calculate difference
        difference = abs(CurrentDistance - IdealDistance)

        #calc similarity, will never be negative
        similarity = max(0, 1 - difference / DistanceTolerance)


        SumOfDistanceWeightedSimilarties += weight

        weightedSimilarity = similarity * weight

        SumOfDistanceWeightedSimilarties += weightedSimilarity

    finalDistanceScore = SumOfDistanceWeightedSimilarties / SumOfDistanceWeights

    SumOfAngleWeightedSimilarties = 0
    SumOfAngleWeights = 0

    for PairAngles in CurrentHand.pairWiseAngles:
        weight = DBHand.pairWiseAngleWeights[PairAngles]
        CurrentDistance = CurrentHand.pairWiseAngles[PairAngles]
        IdealDistance = DBHand.pairWiseAngles[PairAngles]

        # calculate difference
        difference = abs(CurrentDistance - IdealDistance)

        # calc similarity, will never be negative
        similarity = max(0, 1 - difference / AngleTolerance)

        SumOfAngleWeightedSimilarties += weight

        weightedSimilarity = similarity * weight

        SumOfAngleWeightedSimilarties += weightedSimilarity

    finalAngleScore = SumOfAngleWeightedSimilarties / SumOfAngleWeights


    finalScore = (finalDistanceScore + finalAngleScore) / 2 # we can modify this later and weigh angle or distance more if needed

    return finalScore










