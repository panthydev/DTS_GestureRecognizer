from pprint import pprint

import numpy as np
import math

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
    #pprint(distance_Dictionary.keys())

#Creates a key value pair for each point to the other, for distance calculations
    def CreateAngleKeys(self, numHandLandmarks):
        for dict in self.dictAnglesDicts:
            for i in range(numHandLandmarks):
                for k in range(numHandLandmarks):
                    if k > i:
                        key: tuple[int ,int] = (i,k)
                        self.dictAnglesDicts[dict].update({key: 0})
    #pprint(angles_Dictionary.keys())
    #pprint(mediaPipe_Points)

#Udregner distancen mellem to punkter
    def CalulateDistance(self, mediaPipe_Points, dictToUpdate):
        #distance_Dictionary = {}
        #self.CreateDistanceKeys(self, 21, distance_Dictionary)
        for i in range(len(mediaPipe_Points)):
            for k in range(len(mediaPipe_Points)):
                if k > i:
                #x,y,z = mediaPipe_Points[f"{i}"]
                #x2,y2,z2 = mediaPipe_Points[f"{k}"]
                    point_distance = math.sqrt((mediaPipe_Points[i].x + mediaPipe_Points[k].x) ** 2+(mediaPipe_Points[i].y+mediaPipe_Points[k].y) ** 2+(mediaPipe_Points[i].z+mediaPipe_Points[k].z) ** 2)
                    self.dictDistancesDicts[dictToUpdate][i,k] = point_distance
    #pprint(distance_Dictionary)
        return(self.dictDistancesDicts[dictToUpdate])


    def CalulateAngle(self, mediaPipe_Points, dictToUpdate):
        #angles_Dictionary = {}
        #self.CreateAngleKeys(self, 21, angles_Dictionary)
        for i in range(len(mediaPipe_Points)):
            for k in range(len(mediaPipe_Points)):
                if k > i:
                #x,y,z = mediaPipe_Points[f"{i}"]
                #x2,y2,z2 = mediaPipe_Points[f"{k}"]
                    point_angle = math.acos((mediaPipe_Points[i].x*mediaPipe_Points[k].x + mediaPipe_Points[i].y*mediaPipe_Points[k].y + mediaPipe_Points[i].z*mediaPipe_Points[k].z)/(math.sqrt(mediaPipe_Points[i].x ** 2 + mediaPipe_Points[i].y ** 2 + mediaPipe_Points[i].z ** 2) * math.sqrt(mediaPipe_Points[k].x ** 2 + mediaPipe_Points[k].y ** 2 + mediaPipe_Points[k].z ** 2)))
                    point_angle = math.degrees(point_angle) #Remove to get the angle in radians instead of degrees
                    self.dictAnglesDicts[dictToUpdate][i,k] = point_angle
    #pprint(angles_Dictionary)
        return(self.dictAnglesDicts[dictToUpdate])