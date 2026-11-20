from pathlib import Path
import cv2
import DetectHands
from CalculateHands import Calculate_Hands as CalHands
from DetectHands import DetectHands
from Hands_Data import HandsData
import GestureComparitor as GestureCom
import Util
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

    ConfusionMatrix = []
    handsDataList = []

    Otherindex = 0
    for subDir in subDirs:
        Otherindex += 1
        imageList = []

        Dict = {}
        OtherDict = {}


        for i in range(65, 65+25):
            if i == 74 : continue
            letter = chr(i)
            OtherDict[str(letter)] = 0
        OtherDict[str(chr(198))] = 0
        Dict[str(subDir.name)] = OtherDict
        ConfusionMatrix.append(Dict)

        print("Reading images from:" + str(subDir))
        for image in subDir.iterdir():
            if image.is_file():
                cvImage = cv2.imread(str(image))

                detectionResults = DetectHands.DetectHandsImage(DetectHands, cvImage)
                if len(detectionResults.hand_world_landmarks) == 0:
                    image.unlink()
                    continue
                imageList.append(cvImage)

        for image in imageList:
            print("Creating Hand data for individual image")
            handsData = HandsData()
            detectionResults = DetectHands.DetectHandsImage(DetectHands, image)

            handsData.UpdateHandObjects(detectionResults)
            handsDataList.append(handsData)


        f1 = open(str(subDir.name) + ".txt", "w")
        for handsData in handsDataList:
            print("running comparison for each hand")


            closestMatch = GestureCom.CompareHandToAllGestures(handsData, AllhandsData)


            if(subDir.name == "AE"):
                index = 1
                string = closestMatch[1].name.replace("!", "")
               # string = string.lower()
                ConfusionMatrix[index]["AE"][string] += 1
            elif(subDir.name == "K"):
                index = 10
                string = closestMatch[1].name.replace("!", "")
                # string = string.lower()
                ConfusionMatrix[index]["K"][string] += 1
            else:
                index = 65 - ord(subDir.name) -1
                index = abs(index) # could just ue confusion matrix length as index here.
                if index >= 12:
                    index = index -1
                if(index == 1): continue
                string = closestMatch[1].name.replace("!", "")
                ConfusionMatrix[index][subDir.name][string] += 1


            f1.write(str(closestMatch[1]) + str(closestMatch[0]) + "\n")
        f1.close()
    print("Confusion Matrix: " + str(ConfusionMatrix))