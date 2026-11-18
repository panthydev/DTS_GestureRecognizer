import cv2
import DetectHands
from CalculateHands import Calculate_Hands as CalHands
from DetectHands import DetectHands
from Hands_Data import HandsData
import GestureComparitor as GestureCom
import Util
from DB import DBHandler as DBH
import keyboard


def RunLiveComparison():
    global keypressed
    keypressed = False
    cap = cv2.VideoCapture(0)

    CalHands.CreateKeys(CalHands, 42)

    dbHandler = DBH.DBHandler()

    DBHands = dbHandler.GetAllHands()
    for hand in DBHands:
        hand.handOrientation1 = Util.StrToTuple(hand.handOrientation1)
        hand.handOrientation2 = Util.StrToTuple(hand.handOrientation2)

    keyboard.on_press_key("c", lambda _: globals().update(keypressed=True))

    while cap.isOpened():
        ret, imageCaptured = cap.read()
        if ret:
            handsData = HandsData()
            detectionResults = DetectHands.DetectHandsImage(DetectHands, imageCaptured)

            if len(detectionResults.hand_landmarks) == 0:
                FlippedimageCaptured = cv2.flip(imageCaptured, 1)
                FlippedimageCaptured = cv2.putText(FlippedimageCaptured, "Ingen hånd", (35, 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                            (255, 0, 0), 2) 
                cv2.imshow("img", FlippedimageCaptured)
                key = cv2.waitKey(1)
                if key == 27:
                    break
                continue

            handsData.UpdateHandObjects(detectionResults)

            closetsMatch = GestureCom.CompareHandToAllGestures(handsData, DBHands)

            drawnImage = Util.draw_landmarks(imageCaptured, detectionResults)
            
            flippedImage = cv2.flip(drawnImage, 1)

            flippedImage = cv2.putText(flippedImage, str(closetsMatch[0]) + " " + str(closetsMatch[1].name), (35, 35),
                                                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            handsData.image = flippedImage

            if (keypressed):
                keypressed = False
                image = cv2.imwrite("captured gesture.jpg", handsData.image)
                storedHand = dbHandler.SaveHand(handsData)
                print("Capturing gesture, sav)ing to database, exporting image to path: ")

            cv2.imshow("img", flippedImage)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()