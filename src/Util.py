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


def draw_landmarks(img, detection_results): #We use this function to draw the landsmarks the detection result got from the detector function onto the input image
    """Draws the skeleton on the hand(s) present in the image"""
        
    img_copy = np.copy(img)

    for hand_landmarks in detection_results.hand_landmarks: 
        mp_drawing.draw_landmarks(img_copy, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
    return img_copy