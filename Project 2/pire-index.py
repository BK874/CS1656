# Brian Knotten
# CS 1656
# Project 2

# pire-index.py reads all files in a subdirectory "input/" (should all be text
# files), converts all characters to lower case, eliminates punctuation,
# eliminates numbers, performs stemming using the nltk stemmer, and constructs
# an inverted index.
# The inverted index should have for every word: a list of documents the word
# appears in, how many times the words appears per document, a count of how many
# documents the word appears in (in order to compute its inverse document
# frequency), and a count of the total number of documents. This should all be
# stored in a single data structure (dict).
# This data structure should be stored as a json object in a file named:
# "inverted-index.json"

import argparse as argp
import glob
import json
import nltk
import os
import re
import sys


# Process input
parser = argp.ArgumentParser()

# Create inverted index dictionary
invertedIndexDict = {"numDocs":0}

# Read in files, eliminate punctuation and numbers, and perform stemming
# Create dict with, for every word: a list of docs containing the word, num of
# times the word appears per doc, num of docs containing the word, and total
# num of docs.

folder = "input/"
numFiles = 0
for file in os.listdir(folder):
    path = os.path.join(folder, file)
    f = open(path, 'r')
    tokenizer = nltk.RegexpTokenizer(r'[A-Za-z]+')
    myFileTokens = tokenizer.tokenize(f.read())
    porter = nltk.PorterStemmer()
    count = 0
    # For every word in a file
    for token in myFileTokens:
        myFileTokens[count] = str.lower(porter.stem(token))
        # If the word is not in the index, add it and record the document
        if myFileTokens[count] not in invertedIndexDict:
            invertedIndexDict[myFileTokens[count]] = {'docsContaining':[file],
                                                      'numPerDoc':[1],
                                                      'numContaining':1}
        # If the word is in the index and has already appeared in the current
        # document, increment the number of times it appeared in this doc
        elif file in invertedIndexDict[myFileTokens[count]]['docsContaining']:
            fileIndex = \
            invertedIndexDict[myFileTokens[count]]['docsContaining'].index(file)
            invertedIndexDict[myFileTokens[count]]['numPerDoc'][fileIndex] += 1
        # If the word is in the index and this is the first time it appeared in
        # the current doc, add the doc to the list of those containing the word,
        # begin the counter for the num of times it appears in the current doc,
        # and increment the number of docs containing the word
        else:
            invertedIndexDict[myFileTokens[count]]['docsContaining'].append(file)
            invertedIndexDict[myFileTokens[count]]['numPerDoc'].append(1)
            invertedIndexDict[myFileTokens[count]]['numContaining'] += 1
        count += 1
    f.close()
    numFiles += 1
invertedIndexDict["numDocs"] = numFiles

# Dump dict to json
j = open('inverted-index.json', 'w')
json.dump(invertedIndexDict, j)
j.close()
