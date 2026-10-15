import numpy as np
import math
import Util

class Calculate_Hands: 

    rightHandDistances = {} 
    leftHandDistances = {}
    rightHandAngles = {} 
    leftHandAngles = {}

    dictDistancesDicts = {"Right": rightHandDistances, "Left": leftHandDistances}
    dictAnglesDicts = {"Right" : rightHandAngles, "Left": leftHandAngles}

    def CreateKeys(self, numHandLandmarks):
        self.CreateDistanceKeys(self, numHandLandmarks)
        self.CreateAngleKeys(self, numHandLandmarks)

#Creates a key value pair for each point to the other, for distance calculations
    def CreateDistanceKeys(self, numHandLandmarks):
        for dict in self.dictDistancesDicts:
            for i in range(numHandLandmarks):
                for k in range(numHandLandmarks):
                    if k > i:
                        key: tuple[int ,int] = (i,k)
                        self.dictDistancesDicts[dict].update({key: 0})

#Creates a key value pair for each point to the other, for distance calculations
    def CreateAngleKeys(self, numHandLandmarks):
        for dict in self.dictAnglesDicts:
            for i in range(numHandLandmarks):
                for k in range(numHandLandmarks):
                    if k > i:
                        key: tuple[int ,int] = (i,k)
                        self.dictAnglesDicts[dict].update({key: 0})

#Udregner distancen mellem to punkter
    def CalulateDistance(self, landmarks, dictToUpdate) -> dict[str, dict[tuple[int,int], float]] :
        for i in range(len(landmarks)):
            for k in range(len(landmarks)):
                if k > i:
                    #point_distance = math.sqrt((landmarks[i].x - landmarks[k].x) ** 2+(landmarks[i].y-landmarks[k].y) ** 2+(landmarks[i].z-landmarks[k].z) ** 2)
                    point_distance = Util.distanceBetweenPoints(landmarks, i, k)
                    self.dictDistancesDicts[dictToUpdate][i,k] = point_distance
        return(self.dictDistancesDicts[dictToUpdate])


    def CalulateAngle(self, landmarks, dictToUpdate) -> dict[str, dict[tuple[int,int], float]] : 
        for i in range(len(landmarks)):
            for k in range(len(landmarks)):
                if k > i:
                    #point_angle = math.acos((landmarks[i].x*landmarks[k].x + landmarks[i].y*landmarks[k].y + landmarks[i].z*landmarks[k].z)/(math.sqrt(landmarks[i].x ** 2 + landmarks[i].y ** 2 + landmarks[i].z ** 2) * math.sqrt(landmarks[k].x ** 2 + landmarks[k].y ** 2 + landmarks[k].z ** 2)))
                    point_angle = Util.angleBetweenPoints(landmarks, i, k)
                    point_angle = math.degrees(point_angle) #Remove to get the angle in radians instead of degrees
                    self.dictAnglesDicts[dictToUpdate][i,k] = point_angle
        return(self.dictAnglesDicts[dictToUpdate])