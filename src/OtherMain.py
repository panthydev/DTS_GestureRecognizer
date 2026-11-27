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
from WriteCSV import WriteConfidenceMatrix
from WriteCSV import WriteConfusionMatrix


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

        customAlphabetList = ["A", "AE", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]

        for letter in customAlphabetList:
            OtherDict[str(letter)] = 0

        #OtherDict[str(chr(198))] = 0

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

        index = 0
        for handsData in handsDataList:
            
            closestMatch = GestureCom.CompareHandToAllGestures(handsData, AllhandsData)

            ListOfConfidencesSubDir.append(closestMatch[0])

            string = closestMatch[1].name.replace("!", "")

            if(string == "Æ"):
                string = "AE"

            index = customAlphabetList.index(str(subDir.name))

            ConfusionMatrix[index][subDir.name][string] += 1
            ShowEvalComparison(subDir.name, string)
            

        for confidence in ListOfConfidencesSubDir:
            confidenceForSubDir += confidence

        confidenceForSubDir = confidenceForSubDir / len(ListOfConfidencesSubDir)

        confidenceForSubDir = f'{confidenceForSubDir:.2%}'

        ConfidenceList.append(confidenceForSubDir)

    WriteConfusionMatrix(ConfusionMatrix, ResultDirectory)
    WriteConfidenceMatrix(ConfidenceList, ResultDirectory)