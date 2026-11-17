from typing import List
import Hands_Data
import hand
from hand import Hand
from Hands_Data import HandsData

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



    handOrientationList = [CurrentHand.handOrientation1, CurrentHand.handOrientation2]
    OrientationSimilarityScore = 0
    SumOfCoordinateWeights = 0
    SumOfCoordinateWeightedSimilarties = 0

    orientationlist = [DBHand.handOrientation1, DBHand.handOrientation2]
    for handOrientation in handOrientationList:
        #implemet custom check for multi hand gesture, like the other for loops
        otherIndex = 0
        for coordinates in handOrientation:
            index = 0
            
            #weight = DBHand.pairWiseDistanceWeights[PairDistance]
            #CurrentDistance = CurrentHand.pairWiseDistances[PairDistance]
            #IdealDistance = DBHand.pairWiseDistances[PairDistance]

            currentCoordinate = coordinates

            idealCoordinate = orientationlist[otherIndex][index]
            index += 1
    
            #calculate difference
            #difference = abs(currentCoordinate - idealCoordinate)
    
            #calc similarity, will never be negative
            #similarity = max(0, (1 - difference) / 1)
            similarity += 1 - ((abs(currentCoordinate - idealCoordinate)) / (abs((currentCoordinate + idealCoordinate))/2))
        otherIndex += 1

    finalOrientationSimilarityScore = similarity / 3

    finalScore = (finalDistanceScore + finalAngleScore + finalOrientationSimilarityScore) / 3 # we can modify this later and weigh angle or distance more if needed

    return finalScore










