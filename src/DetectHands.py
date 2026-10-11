import mediapipe as mp
import cv2
from mediapipe.tasks import python
import numpy as np
import math
from pprint import pprint
import CalculateHands as CalHand
from hand import Hand

base_options = python.BaseOptions(model_asset_path="src\hand_landmarker.task")
options = mp.tasks.vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = mp.tasks.vision.HandLandmarker.create_from_options(options)

mp_drawing = mp.tasks.vision.drawing_utils
mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing_styles = mp.tasks.vision.drawing_styles

class DetectHands:

    detection_result = None
    
    def draw_landmarks(img, detection_results):
        img_copy = np.copy(img)

        for hand_landmarks in detection_results.hand_landmarks:
            mp_drawing.draw_landmarks(img_copy, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
        return img_copy

    def UpdateHandData(self, handToUpdate, handsData, handIndex):
        if(handToUpdate == "Right"):
            handsData.rightHand.rawPositions = self.detection_result.hand_landmarks[handIndex]
            handsData.rightHand.handFactor = self.detection_result.handedness[handIndex][0].score

            handsData.rightHand.pairWiseAngles = CalHand.CalulateAngle(self.detection_result.hand_landmarks[handIndex])
            handsData.rightHand.pairWiseDistances = CalHand.CalulateDistance(self.detection_result.hand_landmarks[handIndex])

        elif(handToUpdate == "Left"):
            handsData.leftHand.rawPositions = self.detection_result.hand_landmarks[handIndex]
            handsData.leftHand.handFactor = self.detection_result.handedness[handIndex][0].score

            handsData.leftHand.pairWiseAngles = CalHand.CalulateAngle(self.detection_result.hand_landmarks[handIndex])
            handsData.leftHand.pairWiseDistances = CalHand.CalulateDistance(self.detection_result.hand_landmarks[handIndex])
            

    def CheckForHandToUpdate(self, handsData):
        handDetected = None
        for hand in range(len(self.detection_result.handedness)):
            if(self.detection_result.handedness[hand][0].display_name == "Right"):
                handDetected = "Right"
                self.UpdateHandData(DetectHands, handDetected, handsData, hand)
            else:   
                handDetected = "Left"
                self.UpdateHandData(DetectHands, handDetected, handsData, hand)


    def HandsDetect(self, image, handsData):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        self.detection_result = detector.detect(img)

        self.CheckForHandToUpdate(DetectHands, handsData)

        drawn_image = self.draw_landmarks(img.numpy_view(), self.detection_result)

        return cv2.cvtColor(drawn_image, cv2.COLOR_RGB2BGR)
