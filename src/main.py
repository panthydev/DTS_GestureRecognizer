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

def RunLiveComparison():
    cap = cv2.VideoCapture(0)

    CalHands.CreateKeys(CalHands, 42)

    dbHandler = DBH.DBHandler()

    DBHands = dbHandler.GetAllHands()

    keyboard.on_press_key("c", lambda _: globals().update(keypressed=True))
    keypressed = False

    while cap.isOpened():
        ret, imageCaptured = cap.read()
        if ret:
            handsData = HandsData()
            detectionResults = DetectHands.DetectHandsImage(DetectHands, imageCaptured)

            if len(detectionResults.hand_landmarks) == 0:
                imageCaptured = cv2.putText(imageCaptured, "Ingen hånd", (35, 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                            (255, 0, 0), 2)
                cv2.imshow("img", imageCaptured)
                key = cv2.waitKey(1)
                if key == 27:
                    break
                continue

            handsData.UpdateHandObjects(detectionResults)

            Hand: HandsData = dbHandler.GetHandById(4)

            List = [Hand]

            closetsMatch = GestureCom.CompareHandToAllGestures(handsData, DBHands)

            drawnImage = Util.draw_landmarks(imageCaptured, detectionResults)
            drawnImage = cv2.putText(drawnImage, str(closetsMatch[0]) + " " + str(closetsMatch[1].name), (35, 35),
                                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            handsData.image = drawnImage

            if (keypressed):
                keypressed = False
                image = cv2.imwrite("captured gesture.jpg", handsData.image)
                storedHand = dbHandler.SaveHand(handsData)
                print("Capturing gesture, sav)ing to database, exporting image to path: ")

            cv2.imshow("img", drawnImage)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()