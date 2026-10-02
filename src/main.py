import cv2
import DetectHands

def DetectHands(imageCaptured):
    DetectHands.DetectHands(imageCaptured)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, imageCaptured = cap.read()
    if ret:
        landmarkImage = DetectHands(imageCaptured)
        flipped_img = cv2.flip(landmarkImage, 1)
        cv2.imshow("img", flipped_img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()