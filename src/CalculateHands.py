import numpy as np
import math
import Util

class Calculate_Hands: 

    distanceWeightsDict = {}
    angleWeightsDict = {}

    ListOfDicts = [distanceWeightsDict, angleWeightsDict]

    def CreateKeys(self, numHandLandmarks):
        for list in self.ListOfDicts:
            for i in range(numHandLandmarks):
                for k in range(numHandLandmarks):
                    if k > i:
                        key: tuple[int ,int] = (i,k)
                        list.update({key: 0.5})

#Udregner distancen mellem to punkter
    def CalulateDistance(self, landmarks) -> dict[tuple[int,int], float] :
        distancesDict = {}
        for i in range(len(landmarks)):
            for k in range(len(landmarks)):
                if k > i:
                    point_distance = Util.distanceBetweenPoints(landmarks, i, k)
                    distancesDict[i,k] = point_distance
        return(distancesDict)

    def CalulateAngle(self, landmarks) -> dict[tuple[int,int], float] :
        anglesDict = {} 
        for i in range(len(landmarks)):
            for k in range(len(landmarks)):
                if k > i:
                    point_angle = Util.angleBetweenPoints(landmarks, i, k)
                    point_angle = math.degrees(point_angle) #Remove to get the angle in radians instead of degrees
                    anglesDict[i,k] = point_angle
        return(anglesDict)

    def AssignWeightDistance(self, landmarks) -> dict[tuple[int,int], float]:
        for i in range(landmarks):
            for k in range(landmarks):
                if k > i:
                    self.distanceWeightsDict[i,k] = 1
        return(self.distanceWeightsDict)

    def AssignWeightAngles(self, landmarks) -> dict[tuple[int,int], float]:
        for i in range(landmarks):
            for k in range(landmarks):
                if k > i:
                    self.angleWeightsDict[i,k] = 1
        return(self.angleWeightsDict)