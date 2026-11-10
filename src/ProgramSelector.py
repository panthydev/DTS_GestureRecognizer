import sys

import DatasetCreation
import main


# print("Creating dataset from images at input path: " + "C:\\Users\\adamc\\Desktop\\GestureAlphabet\\Data\\Alphabet" )
# DatasetCreation.RunDataSetCreation("C:\\Users\\adamc\\Desktop\\GestureAlphabet\\Data\\Alphabet")

if len(sys.argv)>1:
    if sys.argv[1] == "-LC" or sys.argv[1] == "-LiveComparison":
        print("Running LiveComparison")
        print("Total arguments:", len(sys.argv))
        main.RunLiveComparison()
    elif sys.argv[1] == "-help" or sys.argv[1] == "-h" or sys.argv[1] == "help":
        print("You can run ProgramSelector with these launch options: blah blah blah")
    elif sys.argv[1] == "-ML" or sys.argv[1] == "-MachineLearning":
        if 3 == len(sys.argv):
            #check if path is actually a valid path
            print("Total arguments:", len(sys.argv))
            print("Creating dataset from images at input path: " + sys.argv[2])
            DatasetCreation.RunDataSetCreation(sys.argv[2])