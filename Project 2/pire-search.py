# Brian Knotten
# CS 1656
# Project 2

# pire-search.py reads he json object from file 'inverted-index.json' and a set of
# keywoards from file 'keywords.txt' and produce an ordered list of document
# filenames, along with their relevance scores and a breakdown of weights for all
# keywords.
# The relevance score for each document is computed as:
# w(key, doc) = (1 + log2(freq(key, doc)) * log2(N/n(doc))
# where n(doc) is the number of documents that contain keyword key and N is the
# total number of documents

import argparse as argp
import collections
import json
import math
import nltk

# Process input
parser = argp.ArgumentParser()

# Read in inverted-index JSON object
j = open('inverted-index.json', 'r')
invIndDic = json.load(j)
j.close()

# Read in the keywords
fileName = "keywords.txt"
k = open(fileName, 'r')
porter = nltk.PorterStemmer()

# Process each set of keywords
for line in k:
    keywords = nltk.word_tokenize(line)
    keywords = list(set(keywords))
    print("------------------------------------------------------------")
    print("keywords = ", end=" ")
    weights = {}
    sortedWeights = {}
    docTotals = {}
    # Process each word of the keywords
    for word in keywords:
        print(str.lower(word), end=" ")
        # Stem words in order to access inverted index dict
        searchWord = str.lower(porter.stem(word))
        weights[word] = {}
        docCount = 0
        # Calculate the weight of each document containing the word
        for doc in invIndDic[searchWord]['docsContaining']:
            weights[word][doc] = \
            ((1+math.log2(invIndDic[searchWord]['numPerDoc'][docCount])) *
             math.log2(invIndDic['numDocs'] /
                       len(invIndDic[searchWord]['docsContaining'])))
            docCount += 1
        # Sort the docs by the weight (max->min)
        sortedWeights[word] = \
            collections.OrderedDict((sorted(weights[word].items(),
                                            key=lambda x: x[1])))

    print("\n")
        
    # Sum the weights for each document and sort
    docTotals = collections.Counter({})
    for w in sortedWeights:
        docTotals = docTotals + collections.Counter(sortedWeights[w])
    
    sortedDocTotals = sorted(docTotals.items(), key=lambda y: y[1], reverse=True)

    printCount = 0
    previous = -1
    for doc in sortedDocTotals:
        
        if previous != doc[1]:
            printCount += 1
        previous = doc[1]
        
        print("[%d] file=%s score =%f" %(printCount, doc[0], doc[1]))
        for word in keywords:
            if doc[0] in sortedWeights[word]:
                print("weight(%s)=%f" %(str.lower(word),
                                        sortedWeights[word][doc[0]]))
            else:
                print("weight(%s)=0.000000" %(str.lower(word)))

        
        print("\n", end="")
        
