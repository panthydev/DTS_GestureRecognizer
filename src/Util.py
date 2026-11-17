import math
import numpy as np
import mediapipe as mp

mp_drawing = mp.tasks.vision.drawing_utils
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing_styles = mp.tasks.vision.drawing_styles


def dict_to_json(data):
    return {f"{i},{j}": value for (i, j), value in data.items()}


def json_to_dict(data):
    return {
        tuple(map(int, key.split(","))): value
        for key, value in data.items()
    }

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

def calculateVectorLenght(vector : tuple[float, float, float]):
    #listToUse = [1, 4 ,6]
    #newTuple = tuple(listToUse)

    #newTuple = (1, 4 ,6)
    
    vectorLenght = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    return vectorLenght


def normalizeVector(nonNormVector : tuple[float, float, float]):
    vectorLenght = calculateVectorLenght(nonNormVector)

    normVector = [nonNormVector[0]/vectorLenght, nonNormVector[1]/vectorLenght, nonNormVector[2]/vectorLenght]

    normVector = tuple(normVector)

    return normVector


def draw_landmarks(img, detection_results): #We use this function to draw the landsmarks the detection result got from the detector function onto the input image
    """Draws the skeleton on the hand(s) present in the image"""
        
    img_copy = np.copy(img)

    for hand_landmarks in detection_results.hand_landmarks: 
        mp_drawing.draw_landmarks(img_copy, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
    return img_copy

def StrToTuple(inputTupleString):
    strList = []
    for element in inputTupleString:
        strList.append(element)

    strList.pop(0)
    strList.pop(len(strList) - 1)
    strList.append(",")

    floatList : list[str, str, str] = []
    string = "" 
    for element in strList:
        if(element == ","):
            floatList.append(string)
            string = ""
        else:
            string += element

    index = 0
    for str in floatList:
        floatList[index] = float(str)
        index +=1

    return tuple(floatList)