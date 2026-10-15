import math

class Utils:

    def distanceBetweenPoints(landmarks, point2, point1) -> float:
        pointDistance = math.sqrt((landmarks[point2].x - landmarks[point1].x) ** 2+(landmarks[point2].y-landmarks[point1].y) ** 2+(landmarks[point2].z-landmarks[point1].z) ** 2)
        return pointDistance

    def angleBetweenPoints(landmarks, point2, point1) -> float:
        pointAngle = math.acos((landmarks[point2].x*landmarks[point1].x + landmarks[point2].y*landmarks[point1].y + landmarks[point2].z*landmarks[point1].z)/(math.sqrt(landmarks[point2].x ** 2 + landmarks[point2].y ** 2 + landmarks[point2].z ** 2) * math.sqrt(landmarks[point1].x ** 2 + landmarks[point1].y ** 2 + landmarks[point1].z ** 2)))
        return pointAngle