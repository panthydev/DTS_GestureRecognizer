import hand
from hand import Hand

DistanceTolerance = 0.1



# should actually return key to gesture in DB that matches or the match directly
def CompareHandToGestureHand(CurrentHand : Hand, DBHand : Hand) -> float:

    SumOfWeightedSimilarties = 0
    SumOfWeights = 0
    SumOfWeights = sum(DBHand.pairWiseDistanceWeights.values()) # this probably doesnt work

    #PairDistance is the key
    for PairDistance in CurrentHand.pairWiseDistances:

        CurrentDistance = CurrentHand.pairWiseDistances[PairDistance]
        IdealDistance = DBHand.pairWiseDistances[PairDistance]

        #calculate difference
        difference = abs(CurrentDistance - IdealDistance)

        #calc similarity, will always be between 0 and 1
        similarity = max(0, 1 - difference / DistanceTolerance)

        weightedSimilarity = similarity * DBHand.pairWiseDistanceWeights[PairDistance]
        SumOfWeightedSimilarties += weightedSimilarity

    finalScore = SumOfWeightedSimilarties / SumOfWeights
    return finalScore





