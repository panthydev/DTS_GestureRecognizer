import hand
from hand import Hand

DistanceTolerance = 0.1



# should actually return key to gesture in DB that matches or the match directly
def CompareHandToGestureHand(CurrentHand : Hand, DBHand : Hand) -> float:

    SumOfWeightedSimilarties = 0
    SumOfWeights = 0
    SumOfWeights = 0

    #PairDistance is the key
    for PairDistance in CurrentHand.pairWiseDistances:

        weight = DBHand.pairWiseDistanceWeights[PairDistance]
        CurrentDistance = CurrentHand.pairWiseDistances[PairDistance]
        IdealDistance = DBHand.pairWiseDistances[PairDistance]


        #calculate difference
        difference = abs(CurrentDistance - IdealDistance)

        #calc similarity, will never be negative
        similarity = max(0, 1 - difference / DistanceTolerance)


        SumOfWeightedSimilarties += weight

        weightedSimilarity = similarity * weight

        SumOfWeightedSimilarties += weightedSimilarity

    finalScore = SumOfWeightedSimilarties / SumOfWeights
    return finalScore





