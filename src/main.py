import cv2
import DetectHands
from hand import Hand
from CalculateHands import Calculate_Hands as CalHands
from DetectHands import DetectHands
from Hands_Data import HandsData
import GestureComparitor as GestureCom
import Util

handsData = HandsData()

cap = cv2.VideoCapture(0)

CalHands.CreateKeys(CalHands, 42)

while cap.isOpened():
    ret, imageCaptured = cap.read()
    if ret:
        detectionResults = DetectHands.DetectHandsImage(DetectHands, imageCaptured)
        handsData.UpdateHandObjects(detectionResults)
        
        drawnImage = Util.draw_landmarks(imageCaptured, detectionResults)
        #drawnImage = cv2.putText(drawnImage, closetsMatch[0] + " " + str(closetsMatch[1]), (35, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
       
        cv2.imshow("img", drawnImage)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()