import csv
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


def RunDataCreation(imageList: list[np.ndarray]) -> list[HandsData]:
    CalHands.CreateKeys(CalHands, 42)
    handsDataList = []

    for image in imageList:
        handsData = HandsData()
        detectionResults = DetectHands.DetectHandsImage(DetectHands, image)

        handsData.UpdateHandObjects(detectionResults)
        handsDataList.append(handsData)

    return handsDataList


def ShowEvalComparison(CurrentDirString, EvaluatedGestureString):
    print("CORRECT LETTER: " + str(CurrentDirString) + ", GUESSED LETTER: " + str(EvaluatedGestureString))


def RunImageEvaluation(path: str):
    dbHandler = DBH()
    AllhandsData = dbHandler.GetAllHands()

    for hand in AllhandsData:
        hand.handOrientation1 = Util.StrToTuple(hand.handOrientation1)
        hand.handOrientation2 = Util.StrToTuple(hand.handOrientation2)

    path = Path(path)
    print("Path:", path)

    ResultDirectory = Path("HandCraftedResults")
    ResultDirectory.mkdir(exist_ok=True, parents=True)  # creates result folder

    subDirs = [f for f in path.iterdir() if f.is_dir()]

    ConfusionMatrix = []
    ConfidenceList = [] 

    Otherindex = 0
    for subDir in subDirs:
        handsDataList = []
        Otherindex += 1
        imageList = []
        
        confidenceForSubDir = 0

        ListOfConfidencesSubDir = []

        Dict = {}
        OtherDict = {}

        for i in range(65, 65 + 25):
            if i == 74: continue
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
            handsData = HandsData()
            detectionResults = DetectHands.DetectHandsImage(DetectHands, image)

            handsData.UpdateHandObjects(detectionResults)
            handsDataList.append(handsData)

        for handsData in handsDataList:

            closestMatch = GestureCom.CompareHandToAllGestures(handsData, AllhandsData)

            ListOfConfidencesSubDir.append(closestMatch[0])


            if (subDir.name == "AE"):
                index = 1
                string = closestMatch[1].name.replace("!", "")
                # string = string.lower()
                ConfusionMatrix[index]["AE"][string] += 1

                ShowEvalComparison(subDir.name, string)
            elif (subDir.name == "K"):
                index = 10
                string = closestMatch[1].name.replace("!", "")
                # string = string.lower()
                ConfusionMatrix[index]["K"][string] += 1

                ShowEvalComparison(subDir.name, string)
            elif (subDir.name == "A"):
                index = 0
                string = closestMatch[1].name.replace("!", "")
                ConfusionMatrix[index][subDir.name][string] += 1
                ShowEvalComparison(subDir.name, string)
            else:
                index = 65 - ord(subDir.name) - 1
                index = abs(index)  # could just ue confusion matrix length as index here.
                if index >= 12:
                    index = index - 1
                if (index == 1): continue
                string = closestMatch[1].name.replace("!", "")
                ConfusionMatrix[index][subDir.name][string] += 1
                ShowEvalComparison(subDir.name, string)

        for confidence in ListOfConfidencesSubDir:
            confidenceForSubDir += confidence

        confidenceForSubDir = confidenceForSubDir / len(ListOfConfidencesSubDir)

        confidenceForSubDir = f'{confidenceForSubDir:.2%}'

        ConfidenceList.append(confidenceForSubDir)


    with open(ResultDirectory / f"ConfusionMatrix.csv", "w", newline='') as csvFile:
        fieldnames1 = [" IGNORE "]

        CustomAlphabetList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R",
                              "S", "T", "U", "V", "W", "X", "Y", "Æ"]

        fieldnames = [l for l in CustomAlphabetList]
        fieldnames1.extend(fieldnames)

        writer = csv.writer(csvFile)
        writer.writerow(fieldnames1)

        ÆDict = ConfusionMatrix.pop(1)
        newKVP = {"Æ" : ÆDict["AE"] }
        ConfusionMatrix.append(newKVP)



        for outerDictionary in ConfusionMatrix:

            KeyToAccessInnerDictionary = list(outerDictionary.keys())
            KeyToAccessInnerDictionary = KeyToAccessInnerDictionary[0]

            finalList = [str(KeyToAccessInnerDictionary)]

            for value in outerDictionary[KeyToAccessInnerDictionary].values():
                finalList.append(value)
            writer.writerow(finalList)
            continue

    with open(ResultDirectory / f"ConfidenceMatrix.csv", "w", newline='') as csvFile:
            CustomAlphabetList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R",
                                  "S", "T", "U", "V", "W", "X", "Y", "Æ"]
    
            fieldnames = [l for l in CustomAlphabetList]
    
            writer = csv.writer(csvFile)
            writer.writerow(fieldnames)
    
            ÆConfidence = ConfidenceList.pop(1)

            ConfidenceList.append(ÆConfidence)

            writer.writerow(ConfidenceList)

    