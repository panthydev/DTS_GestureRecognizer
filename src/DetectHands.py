import mediapipe as mp
import cv2
from mediapipe.tasks import python
import numpy as np
import math
from pprint import pprint
from CalculateHands import Calculate_Hands as CalHands
from hand import Hand
from Hands_Data import HandsData

base_options = python.BaseOptions(model_asset_path="src\hand_landmarker.task")
options = mp.tasks.vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = mp.tasks.vision.HandLandmarker.create_from_options(options)

mp_drawing = mp.tasks.vision.drawing_utils
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing_styles = mp.tasks.vision.drawing_styles

class DetectHands:

    detection_result = None
    
    def draw_landmarks(img, detection_results): #We use this function to draw the landsmarks the detection result got from the detector function onto the input image
        img_copy = np.copy(img)

        for hand_landmarks in detection_results.hand_landmarks: 
            mp_drawing.draw_landmarks(img_copy, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
        return img_copy


    def HandsDetect(self, image, handsData : HandsData): #We use this function to detect the hands present in the input image 

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #We use this cv2 function to transform the input image into a rgb image

        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb) #we use this function to tranforms the rbg image into a srgb image
        
        self.detection_result = detector.detect(img) #We use this mediapipe function to detect hands in the image and this function returns and array containing information on the detected hands

        handsData.UpdateDirections(self.detection_result) #We then run this method to update the handsdata object based on the data on the hands we got from detection result

        drawn_image = self.draw_landmarks(img.numpy_view(), self.detection_result) #Based on the detection results we got from the detector function we run this method

        return cv2.cvtColor(drawn_image, cv2.COLOR_RGB2BGR) #We then return the image where we have drawn the landmarks on the hand 
