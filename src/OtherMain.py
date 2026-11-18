import DetectHands
from CalculateHands import Calculate_Hands as CalHands
from DetectHands import DetectHands
from Hands_Data import HandsData
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