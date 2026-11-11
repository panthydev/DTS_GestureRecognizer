import csv
import json
import pathlib
import sys
import os
from pathlib import Path

import cv2

import OtherMain


def RunDataSetCreation(path : str):
    path = Path(path)
    print("Path:", path)

    ResultDirectory = Path("Results")
    ResultDirectory.mkdir(exist_ok=True, parents=True) #creates result folder

    subDirs = [f for f in path.iterdir() if f.is_dir()]


    with open(ResultDirectory / f"DATAAAAA", "w", newline='') as csvFile:

        for subDir in subDirs:
            imageList = []


            for image in subDir.iterdir():
                if image.is_file():
                    cvImage = cv2.imread(str(image))
                    imageList.append(cvImage)
            HandsDataList = OtherMain.RunDataCreation(imageList)

            fieldnames = ["Label", "Landmark", "PairwiseDistance", "PairwiseAngle"]
            #writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer = csv.writer(csvFile)
            writer.writerow(fieldnames)
            #writer.writeheader()
            for handsData in HandsDataList:

                rawPositions = {
                    k: (v.x, v.y, v.z)
                    for k, v in handsData.rawPositions.items()
                }
                writer.writerow([f"{subDir.name}",
                                 json.dumps(rawPositions),
                                 json.dumps({str(k): v for k, v in handsData.pairWiseDistances.items()}),
                                 json.dumps({str(k): v for k, v in handsData.pairWiseAngles.items()})])
    print("Complete")