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