import math
import sys
import os
import csv
import re
from collections import defaultdict
import random

# input files directory: C:\Users\oron.werner\PycharmProjects\NLP\hw1Input

directory = r'C:\Users\oron.werner\PycharmProjects\NLP\hw1Output'
outputDir = r'C:\Users\oron.werner\PycharmProjects\NLP\hw2Output'
numOfUsers = 10

# TODO: creats system args for inputDir and file path before sending
def main():  # directory=sys.argv[1], numOfUsers=sys.argv[2], outputDir=sys.argv[3]
    print('*********************************')
    numOfUsersToPrint = int(numOfUsers)
    totalCorpus = []
    tempCorpus = []

    if not os.path.exists(outputDir):  # make output dir if not exists
        os.makedirs(outputDir)

    for currentFile in os.listdir(directory):
        if currentFile.endswith(".txt"):
            path = directory + '\\' + currentFile
            print()
            print('Reading the file: ')
            print(path)

            f = open(path, 'r', encoding='utf-8')
            totalCorpus += f

        print('*********************************')


    for line in totalCorpus:
        tempLine = line.rstrip()
        tempLine += ' <end>\n'

        # print(tempLine)
        tempCorpus.append(tempLine)

    totalCorpus = tempCorpus



    # Creating sentences for Unigrams
    unigramProbabilityInFile, unigramTotalAppearance = calcTokenProbability(totalCorpus)  # for unigram calculation
    # calcSentenceProbability(tokenProbabilityInFile)   # only for the specific sentences probability calculation
    # print('\nUnigrams model based on complete dataset:')
    # printRandomizedSentenceByDistribution(unigramProbabilityInFile)



    # Creating sentences for Bigrams
    tempCorpus = []
    for line in totalCorpus:
        tempLine = line.rstrip()
        tempLine = '<start> ' + tempLine + '\n'

        # print(tempLine)
        tempCorpus.append(tempLine)
    totalCorpus = tempCorpus

    # # TODO: remove file creation before sending. For testing purpose only
    # f = open(outputDir + "\\" + 'test' + '.txt', 'w+', encoding='utf-8')  # creates a file with all users for testings
    # for line in totalCorpus:
    #     f.write(line)

    bigramProbabilityInFile = calcTokenProbabilityBigram(totalCorpus, unigramTotalAppearance)
    for k in sorted(bigramProbabilityInFile, key=bigramProbabilityInFile.get, reverse=False):
        print(k, bigramProbabilityInFile[k])



def calcTokenProbabilityBigram(totalCorpus, unigramTotalAppearance):

    bigramAppearance, totalBigramsNum = createTokenAppearanceDictBigram(totalCorpus)  # return a token appearance dict, and the total number of words

    # for k in sorted(tokenAppearance, key=tokenAppearance.get, reverse=False):
    #     print(k, tokenAppearance[k])

    vocabularySize = len(bigramAppearance)
    print('Len of dict is: ' + str(len(bigramAppearance)))
    print('Total number of Bigrams: ' + str(totalBigramsNum))

    bigramProbabilityInFile = bigramAppearance.copy()

    for token in bigramProbabilityInFile:
        if token.split()[0] in unigramTotalAppearance:
            # print(token + ' | ' + token.split()[0])
            bigramProbabilityInFile[token] = (bigramAppearance[token]/(unigramTotalAppearance[token.split()[0]] + vocabularySize))
        else:
            bigramProbabilityInFile[token] = (bigramAppearance[token] / (unigramTotalAppearance['<unk>'] + vocabularySize))
            # TODO: add case of call back -> use unknown token

    # reconstructedTokenCount
#     TODO: Check if should work with log
#     for k in sorted(tokenProbabilityInFile, key=tokenProbabilityInFile.get, reverse=False):
#         print(k, tokenProbabilityInFile[k])

    return bigramProbabilityInFile


def createTokenAppearanceDictBigram(totalCorpus):
    totalBigrams = 0
    tokenAppearance = {}

    # TODO: remove list limitation
    for line in totalCorpus:
        for word, nextWord in zip(line.split()[:-1], line.split()[1:]):
            if word.lower() + ' ' + nextWord.lower() not in tokenAppearance:
                tokenAppearance[word.lower() + ' ' + nextWord.lower()] = 2   # added another 1 for laplace smoothing
                totalBigrams += 1
            else:
                tokenAppearance[word.lower() + ' ' + nextWord.lower()] += 1

    # tokenAppearance['<unk>'] = 1    # added the unknown token for laplace smoothing
    # totalBigrams += 1     # unknown token was added to vocabulary

    # print(tokenAppearance)

    return tokenAppearance, totalBigrams




def calcTokenProbability(totalCorpus):

    tokenAppearance, totalWords = createTokenAppearanceDict(totalCorpus)  # return a token appearance dict, and the total number of words

    # for k in sorted(tokenAppearance, key=tokenAppearance.get, reverse=False):
    #     print(k, tokenAppearance[k])

    vocabularySize = len(tokenAppearance)
    print('Len of dict is: ' + str(len(tokenAppearance)))
    print('Total number of words: ' + str(totalWords))

    tokenProbabilityInFile = tokenAppearance.copy()
    tokenReconstructedCounts = tokenProbabilityInFile.copy()

    for token in tokenProbabilityInFile:
        tokenProbabilityInFile[token] = (tokenAppearance[token]/(totalWords + vocabularySize))

    for token in tokenReconstructedCounts:
        tokenReconstructedCounts[token] = (tokenAppearance[token]/(totalWords + vocabularySize)) * totalWords
    # reconstructedTokenCount
#     TODO: Check if should work with log
#     for k in sorted(tokenProbabilityInFile, key=tokenProbabilityInFile.get, reverse=False):
#         print(k, tokenProbabilityInFile[k])

    return tokenProbabilityInFile, tokenAppearance



def printRandomizedSentenceByDistribution(tokenProbabilityInFile):

    for i in range(3):
        sentence = createRandomizedSentenceByDistribution(tokenProbabilityInFile)
        for word in sentence:
            print(word + ' ', end='')
        print()


def createRandomizedSentenceByDistribution(tokenProbabilityInFile):
    sentence = []
    word = ''
    while word != '<end>':
        word = randomWordByDistribution(tokenProbabilityInFile)
        sentence.append(word)
    return sentence


def randomWordByDistribution(tokenProbabilityInFile):
    rand_val = random.random()
    # print('rand value is: ' + str(rand_val))
    total = 0
    # word = '<start>'

    # while word != '<end>':
    for k, v in tokenProbabilityInFile.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'


def calcSentenceProbability(tokenProbabilityInFile):

    probabilitySum = 0  # this will calculate the sum of the Log2 probabilities for the sentence
    sentences = []

    sentences.append('I don \' t think so . . .')
    sentences.append('Fake news !')
    sentences.append('There is no place like home .')
    sentences.append('Aabbcc hello abc')

    for sentence in sentences:
        sentenceToCalc = sentence.split()
        for word in sentenceToCalc:
            if word.lower() not in tokenProbabilityInFile:
                print('\n*****************************************************************')
                print('Word: \'' + word.lower() + '\' is not in dictionary. Changed to <unk>')
                print('*****************************************************************')
                word = '<unk>'
            if probabilitySum == 0:
                probabilitySum = tokenProbabilityInFile[word.lower()]
            else:
                probabilitySum *= tokenProbabilityInFile[word.lower()]
        print('\nSentence: \"' + sentence + '\" | probability is: ' + str((probabilitySum)))



def createTokenAppearanceDict(totalCorpus):
    totalWords = 0
    tokenAppearance = {}

    # for currentFile in os.listdir(outputDir):
    #     if currentFile.endswith(".txt"):
    #         path = outputDir + '\\' + currentFile
    #         print(path)
    #         with open(path, 'r', encoding='utf-8') as file:

    # TODO: remove list limitation
    for line in totalCorpus:
        for word in line.split():
            totalWords += 1
            if word.lower() not in tokenAppearance:
                tokenAppearance[word.lower()] = 2   # added another 1 for laplace smoothing
            else:
                tokenAppearance[word.lower()] += 1

    tokenAppearance['<unk>'] = 1    # added the unknown token for laplace smoothing
    totalWords += 1     # unknown token was added to vocabulary

    # print(tokenAppearance)

    return tokenAppearance, totalWords


main()
