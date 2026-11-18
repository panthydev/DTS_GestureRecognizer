from typing import List
import Hands_Data
import hand
from hand import Hand
from Hands_Data import HandsData
import NewMath

DistanceTolerance = 0.1
AngleTolerance = 1

# general notes:
# Earlier version didn't take into account multi hand gesture, this one does, although i had to torture hands_data to achieve it
# basically Hands_Data now acts like a hand... it made the switch to multi hand gesture support very easy
# Hands_Data has the variables for it, although the functionality isn't implemented yet, but shouldn't take too long, its just adding together -
# the pair wise calculations from the left and right hand, so its all in one dictionary, so we have 42 landmarks i guess ?
# we effectively have "one big hand" lmao, formed from the two hands
# this works when there is just 1 hand as well, as the weights account for the lack of half the landmarks


# maybe this function should return the key to the matching gesture in the DB but thats for later
# returns a tuple that has the gesture that "won" and its score
def CompareHandToAllGestures(CurrentHand : HandsData, AllHands : List[HandsData]) -> tuple[float, HandsData] :

    FinalScoresDict = {} # idk type hints arent working, its a [float, Hands_Data] dictionary

    for HandsDataObj in AllHands:
        #run comparison to gesture and add to the final dictionary
        Score =  CompareGestureToDBGesture(CurrentHand, HandsDataObj)
        FinalScoresDict[Score] = HandsDataObj

    closestMatch = (max(FinalScoresDict), FinalScoresDict[max(FinalScoresDict)])
    return closestMatch

def KeySafetyCheck(CurrentKey : tuple[int, int],  DBHand : HandsData) -> bool:

    if CurrentKey in DBHand.pairWiseDistances:
        return True
    else :
        return False



# returns the "score" IE how well a gesture matches the DB gesture
def CompareGestureToDBGesture(CurrentHand : HandsData, DBHand : HandsData) -> float:

    SumOfDistanceWeightedSimilarties = 0
    SumOfDistanceWeights = 0


    #PairDistance is the key
    for PairDistance in CurrentHand.pairWiseDistances:

        if not KeySafetyCheck(PairDistance, DBHand): break

        weight = DBHand.pairWiseDistanceWeights[PairDistance]
        CurrentDistance = CurrentHand.pairWiseDistances[PairDistance]
        IdealDistance = DBHand.pairWiseDistances[PairDistance]


        #calculate difference
        difference = abs(CurrentDistance - IdealDistance)

        #calc similarity, will never be negative
        #similarity = max(0, (1 - difference) / 1)
        similarity = 1 - abs(difference) / (CurrentDistance + IdealDistance)

        SumOfDistanceWeights += weight

        weightedSimilarity = similarity * weight

        SumOfDistanceWeightedSimilarties += weightedSimilarity

    finalDistanceScore = SumOfDistanceWeightedSimilarties / SumOfDistanceWeights

    SumOfAngleWeightedSimilarties = 0
    SumOfAngleWeights = 0

    for PairAngles in CurrentHand.pairWiseAngles:
        if not KeySafetyCheck(PairAngles, DBHand): break
        weight = DBHand.pairWiseAngleWeights[PairAngles]
        CurrentDistance = CurrentHand.pairWiseAngles[PairAngles]
        IdealDistance = DBHand.pairWiseAngles[PairAngles]

        # calculate difference
        difference = abs(CurrentDistance - IdealDistance)

        # calc similarity, will never be negative
        similarity = 1- abs(difference) / (CurrentDistance + IdealDistance)

        SumOfAngleWeights += weight

        weightedSimilarity = similarity * weight

        SumOfAngleWeightedSimilarties += weightedSimilarity

    finalAngleScore = SumOfAngleWeightedSimilarties / SumOfAngleWeights



    DBOrientationList = [DBHand.handOrientation1, DBHand.handOrientation2]
    currentHandOrientationList = []

    if(len(CurrentHand.HandsDictionary["Right"].rawPositions) != 0):
        currentHandOrientationList = [CurrentHand.handOrientation1, CurrentHand.handOrientation2]
        print("Hello")
    else:
        #currentHandOrientationList = [CurrentHand.handOrientation1, NewMath.CalOppositeVector(CurrentHand.handOrientation2)]

        if(abs(CurrentHand.handOrientation1[1]) > 0.8):
            #currentHandOrientationList = [CurrentHand.handOrientation1, NewMath.CalOppositeVector(CurrentHand.handOrientation2)]
            currentHandOrientationList = [CurrentHand.handOrientation1, CurrentHand.handOrientation2]

    finalCosineSimilarityScore = 0

    i = 0
    for currentHandOrientation in currentHandOrientationList:  
        dotProduct = NewMath.DotProduct(currentHandOrientation, DBOrientationList[i])

        cosineSimilarity = dotProduct

        cosineSimilarity = (cosineSimilarity + 1) * 0.5

        finalCosineSimilarityScore += cosineSimilarity

        i += 1

    finalCosineSimilarityScore = finalCosineSimilarityScore / 2

    DistanceWeight = 40
    AngleWeight = 40
    OrientationWeight = 30

    finalScore = ((finalDistanceScore * DistanceWeight) + (finalAngleScore * AngleWeight) + (finalCosineSimilarityScore * OrientationWeight)) / (DistanceWeight + AngleWeight + OrientationWeight) # we can modify this later and weigh angle or distance more if needed

    #finalScore = (finalDistanceScore + finalAngleScore + finalCosineSimilarityScore)/3

    return finalScore










