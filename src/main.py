import cv2
import DetectHands

def Hands_detect(DetectHands, imageCaptured):
    landmarkImage = DetectHands.HandsDetect(DetectHands, imageCaptured)
    return landmarkImage

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, imageCaptured = cap.read()
    if ret:
        landmarkImage = Hands_detect(DetectHands.DetectHands, imageCaptured)
        cv2.imshow("img", landmarkImage)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()