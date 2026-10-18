import hand
from hand import Hand

DistanceTolerance = 0.1



# should actually return key to gesture in DB that matches or the match directly
# currently returns the score of the comparison where 1 is a perfect match and 0 is the worst match possible lmao
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
        similarity = max(0, 1 - difference / DistanceTolerance)

        SumOfAngleWeightedSimilarties += weight

        weightedSimilarity = similarity * weight

        SumOfAngleWeightedSimilarties += weightedSimilarity

    finalAngleScore = SumOfAngleWeightedSimilarties / SumOfAngleWeights


    finalScore = (finalDistanceScore + finalAngleScore) / 2 # we can modify this later and weigh angle or distance more if needed

    return finalScore





