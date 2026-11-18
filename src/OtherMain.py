from pathlib import Path

import cv2
import DetectHands
from hand import Hand
from CalculateHands import Calculate_Hands as CalHands
from DetectHands import DetectHands
from Hands_Data import HandsData
import GestureComparitor as GestureCom
import Util
import msvcrt
import keyboard
from DB.DBHandler import DBHandler as DBH
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

def RunImageEvaluation(path : str):
    dbHandler = DBH()
    AllhandsData = dbHandler.GetAllHands()

    for hand in AllhandsData:
        hand.handOrientation1 = Util.StrToTuple(hand.handOrientation1)
        hand.handOrientation2 = Util.StrToTuple(hand.handOrientation2)

    path = Path(path)
    print("Path:", path)

    ResultDirectory = Path("HandCraftedResults")
    ResultDirectory.mkdir(exist_ok=True, parents=True) #creates result folder

    subDirs = [f for f in path.iterdir() if f.is_dir()]


    handsDataList = []

    for subDir in subDirs:
        imageList = []

        print("Reading images from:" + str(subDir))
        for image in subDir.iterdir():
            if image.is_file():
                cvImage = cv2.imread(str(image))
                imageList.append(cvImage)

        for image in imageList:
            print("Creating Hand data for individual image")
            handsData = HandsData()
            detectionResults = DetectHands.DetectHandsImage(DetectHands, image)

            handsData.UpdateHandObjects(detectionResults)
            handsDataList.append(handsData)

        index = 0
        f1 = open(str(subDir.name) + ".txt", "w")
        for handsData in handsDataList:
            print("running comparison for each hand")
            index += 1

            closestMatch = GestureCom.CompareHandToAllGestures(handsData, AllhandsData)



            f1.write(str(closestMatch[1]) + str(closestMatch[0]) + "\n")
        f1.close()




