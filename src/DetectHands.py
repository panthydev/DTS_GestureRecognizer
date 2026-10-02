import mediapipe as mp
import cv2
from mediapipe.tasks import python
import numpy as np
import math
from pprint import pprint

base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")
options = mp.tasks.vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = mp.tasks.vision.HandLandmarker.create_from_options(options)

mp_drawing = mp.tasks.vision.drawing_utils
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing_styles = mp.tasks.vision.drawing_styles

LandmarkCoordinates = {}

def draw_landmarks(img, detection_results):
    img_copy = np.copy(img)

    for hand_landmarks in detection_results.hand_landmarks:
        mp_drawing.draw_landmarks(img_copy, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
    return img_copy

def Detect_hands(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    detection_result = detector.detect(img)

    drawn_image = draw_landmarks(img.numpy_view(), detection_result)

    try:
        index_tip = detection_result.hand_landmarks[0][8]
        #print(index_tip)
    except:
        print("NO HAND DETECTED")

    try:
        index_tip.x = detection_result.hand_landmarks[0][8].x
        index_tip.y = detection_result.hand_landmarks[0][8].y

        image_width = drawn_image.shape[1]
        image_height = drawn_image.shape[0]
        
        drawn_image2 = cv2.putText(drawn_image, str(index_tip.x), (int(index_tip.x * image_width), int(index_tip.y * image_height)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return cv2.cvtColor(drawn_image2, cv2.COLOR_RGB2BGR)
    except:
        return cv2.cvtColor(drawn_image, cv2.COLOR_RGB2BGR)