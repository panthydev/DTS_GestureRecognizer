import json
import itertools
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

#builds the list with all the 210 pairs and 21 landmarks. Used as the key order for
#distances and angles, so every row is read in the same order
pairs = list(itertools.combinations(range(21), 2))

#Takes a landmark column, a string, and json.loads turns it into a dictionary.
#Flatten takes the x, y, z and turns it into one 'flat' list of 63 numbers
def landmark_vec(s):
    d = json.loads(s)
    return np.array([d[str(i)] for i in range(21)]).flatten()

#str(p) turns the tuple (0, 1) into text "(0, 1)"
def pair_vec(s):
    d = json.loads(s)
    return np.array([d[str(p)] for p in pairs])

def load_csv_data(path="src/ML/Entire_Trainingset.csv"):
    df = pd.read_csv(path)
    X = np.hstack([
        np.stack(df["Landmark"].map(landmark_vec)),
        np.stack(df["PairwiseDistance"].map(pair_vec)),
        np.stack(df["PairwiseAngle"].map(pair_vec)),
    ])
    le = LabelEncoder().fit(df["Label"])
    y = le.transform(df["Label"])
    return X, y, le