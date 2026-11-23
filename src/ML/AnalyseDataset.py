import pandas as pd
import re

# Download and prepare the data
def CleanAndShuffledData(dataset = "DATAAAAA.csv", newDatasetName = "Cleaned_Shuffled_data.csv"):
    """Takes the given dataset and cleans it for empty elements and duplicate headers, then it creates a new dataset which i randomly shuffles

    @param dataset: The given dataset which should be cleaned and shuffled (Note: Remember .csv)
    @param newDatasetName: The name of the new cleaned and shuffled dataset (Note: Remember .csv)
    """
    df = pd.read_csv(dataset)
    for x in df.index:
        if df.loc[x, "Landmark"] == "{}" or df.loc[x, "Landmark"] == "Landmark":
            df.loc[x, "Landmark"] = None
    res = df.dropna().sample(frac=1).reset_index(drop=True) #Remove from .sample if you want to non-randomised
    res.to_csv(newDatasetName, index=False)

#CleanAndShuffledData("csv Data v2\\Training\\training.csv", "Entire_Trainingset.csv")

dataset = pd.read_csv("Entire_Trainingset.csv") #Change string to use other datasets


label = dataset["Label"].values
landmark = dataset["Landmark"].values
pairwiseDistance = dataset["PairwiseDistance"].values
pairwiseAngle = dataset["PairwiseAngle"].values


def SegmentLabel(index = 0):
    """Segments the given dataset for "Label" using index in a string

    @param index: The index of the dataset where the "Label" is optained
    @returns: A string equal to the label in the dataset at the given index
    """
    labelString = label[index]
    return labelString

def SegmentLandmark(index = 0):
    """Segments the given dataset for "Landmark" using index in a list

    @param index: The index of the dataset where the "Landmark" is optained
    @returns: A list containing a tuple for the (x , y, z) coordinates for each landmark
    
    """
    nrLandmark = landmark[index].split(",")
    p = 0
    landmarkList = []
    for i in range(int(len(nrLandmark)/3)):
        x = re.findall(r'-?\d*\.?\d+', nrLandmark[p])
        p += 1
        y = re.findall(r'-?\d*\.?\d+', nrLandmark[p])
        p += 1
        z = re.findall(r'-?\d*\.?\d+', nrLandmark[p])
        p += 1
        landmarkList.append((float(x[1]), float(y[0]), float(z[0])))
    return landmarkList

def SegmentPairwiseDistance(index = 0):
    """Segments the given dataset for "PairwiseDistance" using index in a list

    @param index: The index of the dataset where the "PairwiseDistance" is optained
    @returns: A list containing a tuple for the ("x,y", float(distance)) pairwise distance for each distance calculating. 
    List indexing goes from 0-209, where the pairwise distance key can be got with SegmentPairwiseDistance()[x][0] and just the distance can be got with SegmentPairwiseDistance[x][1]
    """
    nrDistance = pairwiseDistance[index].split(",")
    counter = 0
    distanceList = []
    for i in range(int(len(nrDistance)/2)):
        firstKey = re.findall(r'-?\d*\.?\d+', nrDistance[counter])
        counter += 1
        secondKey = re.findall(r'-?\d*\.?\d+', nrDistance[counter])
        counter += 1
        distanceList.append((f"{firstKey[0]},{secondKey[0]}", float(secondKey[1])))
    return distanceList

def SegmentPairwiseAngle(index = 0):
    """Segments the given dataset for "PairwiseAngle" using index in a list

    @param index: The index of the dataset where the "PairwiseAngle" is optained
    @returns: A list containing a tuple for the ("x,y", float(angle)) pairwise angle for each angle calculating. 
    List indexing goes from 0-209, where the pairwise angle key can be got with SegmentPairwiseAngle()[x][0] and just the angle can be got with SegmentPairwiseAngle[x][1]
    """
    nrAngle = pairwiseAngle[index].split(",")
    counter = 0
    angleList = []
    for i in range(int(len(nrAngle)/2)):
        firstKey = re.findall(r'-?\d*\.?\d+', nrAngle[counter])
        counter += 1
        secondKey = re.findall(r'-?\d*\.?\d+', nrAngle[counter])
        counter += 1
        angleList.append((f"{firstKey[0]},{secondKey[0]}", float(secondKey[1])))
    return angleList

def SegmentDatasetInRowWITHKeys(index = 0):
    """Segments the dataset into rows WITH keyvalues

    @param index: The index of the row in the dataset
    @returns: A list containing the information of the given row
    The label as string. The landmarks as tuple (float, float, float). The key valuepair ("x, y") for distance and distances as float. The key valuepair ("x, y") for angle and angles as float
    
    Note: 
    Can segment into "label" with SegmentDatasetInRowWITHKeys()[0]. 
    Can segment into "landmarks" with SegmentDatasetInRowWITHKeys[1]. 
    Can segment into "Key valuepairs and distances" with SegmentDatasetInRowWITHKeys[2]. 
    Can segment into "Key valuepairs and angles" with SegmentDatasetInRowWITHKeys[3].
    """
    rowList = [SegmentLabel(index), SegmentLandmark(index), SegmentPairwiseDistance(index), SegmentPairwiseAngle(index)]
    return rowList

def SegmentDatasetInRowWITHOUTKeys(index = 0):
    """Segments the dataset into rows WITHOUT keyvalues

    @param index: The index of the row in the dataset
    @returns: A list containing the information of the given row
    The label as string. The landmarks as tuple (float, float, float). The calculated distances as float. The calculated angles as float

    Note: 
    Can segment into "label" with SegmentDatasetInRowWITHKeys()[0]. 
    Can segment into "landmarks" with SegmentDatasetInRowWITHKeys[1]. 
    Can segment into "distances" with SegmentDatasetInRowWITHKeys[2]. 
    Can segment into "angles" with SegmentDatasetInRowWITHKeys[3].
    """
    distances = [t[1] for t in SegmentPairwiseDistance(index)]
    angles = [t[1] for t in SegmentPairwiseAngle(index)]
    
    rowList = [SegmentLabel(index), SegmentLandmark(index), distances, angles]
    return rowList

def GetAmountOfRowsInDataset():
    """Get the amount of rows in the dataset

    @param None
    @returns: The amount of rows in the dataset
    """
    return len(dataset)

def FormatEntireDatasetWITHKeys():
    """Formats the entire dataset like SegmentDatasetInRowWITHKeys()

    @param None
    @returns: The entire dataset as rows, formated like SegmentDatasetInRowWITHKeys(), indexed from 0 to GetAmountOfRowsInDataset()-1 
    """
    rows = []
    for i in range(GetAmountOfRowsInDataset()):
        rows.append(SegmentDatasetInRowWITHKeys(i))
    return rows

def FormatEntireDatasetWITHOUTKeys():
    """Formats the entire dataset like SegmentDatasetInRowWITHOUTKeys()

    @param None
    @returns: The entire dataset as rows, formated like SegmentDatasetInRowWITHOUTKeys(), indexed from 0 to GetAmountOfRowsInDataset()-1 
    """
    rows = []
    for i in range(GetAmountOfRowsInDataset()):
        rows.append(SegmentDatasetInRowWITHOUTKeys(i))
    return rows