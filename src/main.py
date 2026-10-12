import cv2
import DetectHands
from hand import Hand
from CalculateHands import Calculate_Hands as CalHands
from DetectHands import DetectHands
from Hands_Data import HandsData

def Hands_detect(DetectHands, imageCaptured, handsData):
    landmarkImage = DetectHands.HandsDetect(DetectHands, imageCaptured, handsData)
    return landmarkImage

handsData = HandsData()

cap = cv2.VideoCapture(0)

CalHands.CreateKeys(CalHands, 21)

while cap.isOpened():
    ret, imageCaptured = cap.read()
    if ret:
        landmarkImage = Hands_detect(DetectHands, imageCaptured, handsData)
        cv2.imshow("img", landmarkImage)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()