import cv2
import DetectHands
from hand import Hand
from CalculateHands import Calculate_Hands as CalHands
from DetectHands import DetectHands
from Hands_Data import HandsData
import GestureComparitor as GestureCom
import Util
from DB import DBHandler as DBH
import msvcrt
import keyboard
import numpy as np

def RunDataCreation(imageList : list[np.ndarray]) -> list[HandsData]:


    CalHands.CreateKeys(CalHands, 42)
    handsDataList = []

    for image in imageList:
            handsData = HandsData()
            detectionResults = DetectHands.DetectHandsImage(DetectHands, image)

            handsData.UpdateHandObjects(detectionResults)
            handsDataList.append(handsData)


    return handsDataList