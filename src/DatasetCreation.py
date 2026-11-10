import csv
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
    ResultDirectory.mkdir(exist_ok=True, parents=True)

    subDirs = [f for f in path.iterdir() if f.is_dir()]

    for subDir in subDirs:
        with open(ResultDirectory / f"{subDir.name}.csv", "w", newline='') as csvFile:
            csvWriter = csv.writer(csvFile)
            #csvWriter.writerow(["Test", "Pluh"])
            imageList = []

            for image in subDir.iterdir():
                if image.is_file():
                    cvImage = cv2.imread(str(image))
                    imageList.append(cvImage)
            HandsData = OtherMain.RunDataCreation(imageList)

            csvWriter.writerow(HandsData.pairWiseDistances.keys())
            csvWriter.writerow(HandsData.pairWiseDistances.values())

        #    csv.DictWriter(csvFile, HandsData.pairWiseDistances)
          #  csv.DictWriter(csvFile, HandsData.pairWiseAngles)
           # csv.DictWriter(csvFile, HandsData.rawPositions)












    print("Complete")