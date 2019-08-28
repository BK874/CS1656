# Brian Knotten
# CS1656
# Project 5

# decision_tree.py reads in a decision tree stored in a plain text file,
# reads in a test data set stored in a csv file, and evaluates the test
# data using the provided decision tree and provides statistics

import csv
import os
import pandas as pd
import sys

# Helper functions:
# Reads in the tree from a file, removing the newline characters
def readTree(treeInput):
    with open(treeInput) as treeFile:
        lines = treeFile.readlines()
        lines = [x.rstrip() for x in lines if x.rstrip()]
    return lines

# Retreive the a tree line's information
def parseLine(line):
    tokens = line.split(" ")
    tokens = [x for x in tokens if x]
    # Num pipes = depth level
    numPipe = tokens.count("|")
    feature = tokens[numPipe]
    featureVal = tokens[numPipe + 1].strip(":")
    # Category of the final classification
    category = None
    categoryCount = -1
    if (len(tokens) - numPipe) == 4: # If a classification is reached
        category = tokens[numPipe + 2]
        categoryToken = tokens[numPipe+3]
        categoryCount = int(categoryToken[1:len(categoryToken) - 1])
    return (numPipe, feature, featureVal, category, categoryCount)


# Builds a tree in a dictionary
def formTree(treeText):
    tree = {}
    # Keep track of the path that we've travelled down in the tree for the first traversal
    firstLevel = (None, None)
    secondLevel = (None, None)
     # All possible classifications
    possibleDecisions = set([])
    for line in treeText:
        depth, feature, featureVal, category, categoryCount = parseLine(line) # Grab this line's information
        if depth == 0:
            if not feature in tree:
                tree[feature] = {}
                tree[feature][featureVal] = {}
            else:
                if not featureVal in tree[feature]:
                    tree[feature][featureVal] = {}

            if not category is None:
                # Occurence number
                tree[feature][featureVal][category] = 0 
                # New category found
                possibleDecisions.add(category) 

            firstLevel = (feature, featureVal)
            # Reset in case we traversed back up the tree 
            secondLevel = (None, None)
            
        elif depth == 1:
            firstLevelFeat = firstLevel[0]
            firstLevelVal = firstLevel[1]
            if not feature in tree[firstLevelFeat][firstLevelVal]:
                tree[firstLevelFeat][firstLevelVal][feature] = {}
                tree[firstLevelFeat][firstLevelVal][feature][featureVal] = {}
            else:
                if not featureVal in tree[firstLevelFeat][firstLevelVal][feature]:
                    tree[firstLevelFeat][firstLevelVal][feature][featureVal] = {}

            if not category is None:
                # Occurence number
                tree[firstLevelFeat][firstLevelVal][feature][featureVal][category] = 0
                # New category found
                possibleDecisions.add(category)

            secondLevel = (feature, featureVal)
        else: # depth must be 2 (0-based, so we're at level 3)
            firstLevelFeat = firstLevel[0]
            firstLevelVal = firstLevel[1]
            secondLevelFeat = secondLevel[0]
            secondLevelVal = secondLevel[1]

            if not feature in tree[firstLevelFeat][firstLevelVal][secondLevelFeat][secondLevelVal]:
                tree[firstLevelFeat][firstLevelVal][secondLevelFeat][secondLevelVal][feature] = {}
                tree[firstLevelFeat][firstLevelVal][secondLevelFeat][secondLevelVal][feature][featureValue] = {}
            else:
                if not featureValue in tree[firstLevelFeat][firstLevelVal][secondLevelFeat][secondLevelVal][feature]:
                    tree[firstLevelFeat][firstLevelVal][secondLevelFeat][secondLevelVal][feature][featureValue] = {}

            if not category is None:
                # Occurence number
                tree[firstLevelFeat][firstLevelVal][secondLevelFeat][secondLevelVal][feature][featureValue][category] = 0
                # New category found
                possibleDecisions.add(category) 

    # Everything else goes into Unmatched
    tree["UNMATCHED"] = 0
    return (tree, possibleDecisions)


def testTree(tree, dataFile, possibleDecisions):
    # Retreive the test data
    with open(dataFile) as testData:
        data = pd.read_csv(dataFile)
        # For all column names remove the quote and spaces
        data.columns = [column.strip(' "') for column in data.columns]

    columnNames = data.columns
    # For each line in the test file, return to the root of the original tree
    originalTree = tree
    # Iterate through all the rows in the test data set and test each one
    for index, row in data.iterrows():
        path = []
        for i in range(0, 3):
            for column in columnNames:
                # Check if can navigate down the decision tree with this column
                if column in tree:
                    # Retrieve column subtree
                    columnVal = row[column].strip(' \'"')
                    # Check if subtree even
                    if columnVal in tree[column]:
                        # Iteratively navigate
                        tree = tree[column][columnVal]

        # Try to increment the number of occurrences of this test data's information in the tree if we can actually classify it
        foundDecision = False
        # Check if a decision is possible
        for decision in possibleDecisions:
            if decision in tree:
                tree[decision] += 1
                foundDecision = True
                path.append(("decision", decision))
        if not foundDecision:
            originalTree["UNMATCHED"] += 1

        # Reset tree
        tree = originalTree

    return originalTree


# Print the occurences of each lcass in each subtree
def printTrainedTree(treeText, tree, possibleDecisions):
    firstLevel = (None, None)
    secondLevel = (None, None)
    for line in treeText:
        depth, feature, featureValue, category, category_count = parseLine(line)
        if depth == 0:
            subtree = tree[feature][featureValue]

            found_decision = False
            for decision in possibleDecisions:
                if decision in subtree:
                    # Print counts of found decision tree
                    print(feature + " " + str(featureValue) + ": " + decision + " (" + str(subtree[decision]) + ")") 
                    foundDecision = True
            if not foundDecision:
                # Feature to split on found
                print(feature + " " + str(featureValue))

            firstLevel = (feature, featureValue)
            # Reset in case we traversed back up the tree 
            secondLevel = (None, None)
        elif depth == 1:
            firstLevelFeature = firstLevel[0]
            firstLevelValue = firstLevel[1]

            subtree = tree[firstLevelFeature][firstLevelValue][feature][featureValue]
            
            foundDecision = False
            for decision in possibleDecisions:
                if decision in subtree:
                    # Print counts of found decision tree
                    print("|   " + feature + " " + str(featureValue) + ": " + decision + " (" + str(subtree[decision]) + ")") 
                    foundDecision = True
            if not foundDecision:
                # Feature to split on found
                print("|   " + feature + " " + str(featureValue)) 

            secondLevel = (feature, featureValue)
        else:
            firstLevelFeature = firstLevel[0]
            firstLevelValue = firstLevel[1]
            secondLevelFeature = secondLevel[0]
            secondLevelValue = secondLevel[1]

            subtree = tree[firstLevelFeature][firstLevelValue][secondLevelFeature][secondLevelValue][feature][featureValue]

            foundDecision = False
            for decision in possibleDecisions:
                if decision in subtree:
                      # Print counts of found decision tree
                    print("|   |   " + feature + " " + str(featureValue) + ": " + decision + " (" + str(subtree[decision]) + ")") 
                    foundDecision = True
            if not foundDecision:
                 # Feature to split on found
                print("|   |   " + feature + " " + str(featureValue))

    unmatchedVal = tree["UNMATCHED"]
    # If they exist, print unmatched results
    if unmatchedVal > 0: 
        print("UNMATCHED: " + str(tree["UNMATCHED"]))

    return treeText

if not len(sys.argv) == 3:
    print("Invalid number of arguments!")
    sys.exit()
treeInput = sys.argv[1]
testData = sys.argv[2]
if not os.path.exists(treeInput):
    print("Tree file doesn't exist!")
    sys.exit()
elif not os.path.exists(testData):
    print("Test data doesn't exist!")
    sys.exit()

treeText = readTree(treeInput)
trainTree, possibleDecisions = formTree(treeText)
testTree = testTree(trainTree, testData, possibleDecisions)
printTrainedTree(treeText, testTree, possibleDecisions)
