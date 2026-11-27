import csv

def WriteConfusionMatrix(ConfusionMatrix, ResultDirectory):

    with open(ResultDirectory / f"ConfusionMatrix.csv", "w", newline='') as csvFile:
        
        fieldnames1 = [" IGNORE "]
    
        #CustomAlphabetList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R",
                                  #"S", "T", "U", "V", "W", "X", "Y", "Æ"]

        CustomAlphabetList = ["A", "AE", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
        
        fieldnames = [l for l in CustomAlphabetList]
        fieldnames1.extend(fieldnames)
    
        writer = csv.writer(csvFile)
        writer.writerow(fieldnames1)
    
        #ÆDict = ConfusionMatrix.pop(1)
        #newKVP = {"Æ" : ÆDict["AE"] }
        #ConfusionMatrix.append(newKVP)

    
        for outerDictionary in ConfusionMatrix:
    
            KeyToAccessInnerDictionary = list(outerDictionary.keys())
            KeyToAccessInnerDictionary = KeyToAccessInnerDictionary[0]
    
            finalList = [str(KeyToAccessInnerDictionary)]
    
            for value in outerDictionary[KeyToAccessInnerDictionary].values():
                finalList.append(value)
            writer.writerow(finalList)
            continue

def WriteConfidenceMatrix(ConfidenceList, ResultDirectory):
    with open(ResultDirectory / f"ConfidenceMatrix.csv", "w", newline='') as csvFile:
        CustomAlphabetList = ["A", "AE", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]
        
        fieldnames = [l for l in CustomAlphabetList]
        
        writer = csv.writer(csvFile)
        writer.writerow(fieldnames)
    
        writer.writerow(ConfidenceList)