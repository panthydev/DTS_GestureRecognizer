import math

def distanceBetweenPoints(landmarks, point2, point1) -> float:
    pointDistance = math.sqrt((landmarks[point2].x - landmarks[point1].x) ** 2+(landmarks[point2].y-landmarks[point1].y) ** 2+(landmarks[point2].z-landmarks[point1].z) ** 2)
    return pointDistance

def angleBetweenPoints(landmarks, point2, point1) -> float:
    pointAngle = math.acos((landmarks[point2].x*landmarks[point1].x + landmarks[point2].y*landmarks[point1].y + landmarks[point2].z*landmarks[point1].z)/(math.sqrt(landmarks[point2].x ** 2 + landmarks[point2].y ** 2 + landmarks[point2].z ** 2) * math.sqrt(landmarks[point1].x ** 2 + landmarks[point1].y ** 2 + landmarks[point1].z ** 2)))
    return pointAngle

def createVector(point1 : tuple [float, float, float], point2 : tuple[float, float, float]) -> tuple[float, float,float]:
    vector = [point2.x - point1.x, point2.y - point1.y, point2.z - point1.z]
    vector = tuple(vector)
    return vector

def DotProduct(vectorA : tuple, vectorB : tuple) -> float: 
    dotProduct = (vectorA[0] * vectorB[0]) + (vectorA[1] * vectorB[1]) + (vectorA[2] * vectorB[2])
    return dotProduct

def CalOppositeVector(vector : tuple[float, float, float]) -> tuple[float, float, float]:
    oppositeVector = [vector[0] * -1, vector[1] * -1, vector[2] * -1]
    oppositeVector = tuple(oppositeVector)
    return oppositeVector


def calculateVectorLenght(vector : tuple[float, float, float]):
    vectorLenght = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    return vectorLenght


def normalizeVector(nonNormVector : tuple[float, float, float]):


    if nonNormVector[0] == 0 or nonNormVector[1] == 0 or nonNormVector[2] == 0:
        return
    vectorLenght = calculateVectorLenght(nonNormVector)


    normVector = [nonNormVector[0]/vectorLenght, nonNormVector[1]/vectorLenght, nonNormVector[2]/vectorLenght]

    normVector = tuple(normVector)

    return normVector