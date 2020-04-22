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


# TODO: creates system args for inputDir and file path before sending
def main():  # directory=sys.argv[1], numOfUsers=sys.argv[2], outputDir=sys.argv[3]
    print('*********************************')
    numOfUsersToPrint = int(numOfUsers)
    totalCorpus = createCorpus(directory, outputDir)
    # --------------------------------------------------------------------------------------------------------------
    # Creating sentences for Unigrams
    unigramProbabilityInFile, unigramTotalAppearance = calcTokenProbability(totalCorpus)  # for unigram calculation
    # unigramSentenceProbability(unigramProbabilityInFile)   # only for the specific sentences probability calculation
    # print('\nUnigrams model based on complete dataset:')
    # printRandomizedSentenceByDistribution(unigramProbabilityInFile, 'unigrams')
    # --------------------------------------------------------------------------------------------------------------

    # Creating sentences for Bigrams
    tempCorpus = []
    for line in totalCorpus:
        tempLine = line.rstrip()
        tempLine = '<start> ' + tempLine + '\n'
        tempCorpus.append(tempLine)
    totalCorpus = tempCorpus

    # # TODO: remove file creation before sending. For testing purpose only
    # f = open(outputDir + "\\" + 'test' + '.txt', 'w+', encoding='utf-8')  # creates a file with all users for testings
    # for line in totalCorpus:
    #     f.write(line)

    # --------------------------------------------------------------------------------------------------------------
    bigramProbabilityInFile, bigramTotalAppearance = calcTokenProbabilityBigram(totalCorpus, unigramTotalAppearance)
    # bigramSentenceProbability(bigramProbabilityInFile, unigramProbabilityInFile)
    print()
    # printRandomizedSentenceByDistribution(bigramProbabilityInFile, 'bigrams')
    # --------------------------------------------------------------------------------------------------------------



    # --------------------------------------------------------------------------------------------------------------
    trigramProbabilityInFile = calcTokenProbabilityTrigram(totalCorpus, bigramTotalAppearance, unigramProbabilityInFile, bigramProbabilityInFile)
    # print()
    trigramSentenceProbability(trigramProbabilityInFile, bigramProbabilityInFile, unigramProbabilityInFile)
    # printRandomizedSentenceByDistribution(trigramProbabilityInFile, 'trigrams', bigramProbabilityInFile)

    # --------------------------------------------------------------------------------------------------------------



def calcTokenProbabilityTrigram(totalCorpus, bigramTotalAppearance, unigramProbabilityInFile, bigramProbabilityInFile):

    trigramAppearance, totalTrigramsNum = createTokenAppearanceDictTrigram(totalCorpus)  # return a token appearance dict, and the total number of words

    linearInterTrigram = {}

    # for k in sorted(trigramAppearance, key=trigramAppearance.get, reverse=False):
    #     print(k, trigramAppearance[k])

    vocabularySize = len(trigramAppearance)
    print('Len of dict is: ' + str(len(trigramAppearance)))
    print('Total number of Trigrams: ' + str(totalTrigramsNum))

    trigramProbabilityInFile = trigramAppearance.copy()

    for token in trigramProbabilityInFile:
        if token.split()[0] + ' ' + token.split()[1] in bigramTotalAppearance:
            # print(token + ' | ' + token.split()[0] + ' ' + token.split()[1])
            trigramProbabilityInFile[token] = (trigramAppearance[token]/(bigramTotalAppearance[token.split()[0] + ' ' + token.split()[1]] + vocabularySize))
        else:
            trigramProbabilityInFile[token] = (unigramProbabilityInFile['<unk>'])

        # ---------------------------------------------------------------------
        # This part was used to calculate linear interpolation
        # ***********************************************************

        # if token.split()[1] + ' ' + token.split()[2] in bigramProbabilityInFile:
        #     linearBigram = bigramProbabilityInFile[token.split()[1] + ' ' + token.split()[2]]
        # else:
        #     linearBigram = unigramProbabilityInFile['<unk>']
        #
        # if token.split()[2] in unigramProbabilityInFile:
        #     linearUnigram = unigramProbabilityInFile[token.split()[2]]
        # else:
        #     linearUnigram = unigramProbabilityInFile['<unk>']
        #
        # linearSum = trigramProbabilityInFile[token] + linearBigram + linearUnigram
        #
        #
        # linearUnigram /= linearSum
        # linearBigram /= linearSum
        # linearTrigram = trigramProbabilityInFile[token] / linearSum
        #
        # linearUnigram = (0.1) * linearUnigram
        # linearBigram = (0.2) * linearBigram
        # linearTrigram = (0.7) * linearTrigram
        #
        # linearTotal = (linearTrigram + linearBigram + linearUnigram)
        # linearInterTrigram[token] = linearTotal
        # ---------------------------------------------------------------------

#     for k in sorted(trigramProbabilityInFile, key=trigramProbabilityInFile.get, reverse=False):
#         print(k, trigramProbabilityInFile[k])

    return trigramProbabilityInFile



def createTokenAppearanceDictTrigram(totalCorpus):
    totalTrigrams = 0
    tokenAppearance = {}


    for line in totalCorpus:
        for word, nextWord, nextNext in zip(line.split()[:-2], line.split()[1:-1], line.split()[2:]):
            if word.lower() + ' ' + nextWord.lower() + ' ' + nextNext.lower() not in tokenAppearance:
                tokenAppearance[word.lower() + ' ' + nextWord.lower() + ' ' + nextNext.lower()] = 2   # added another 1 for laplace smoothing
                totalTrigrams += 1
            else:
                tokenAppearance[word.lower() + ' ' + nextWord.lower() + ' ' + nextNext.lower()] += 1

    # tokenAppearance['<unk>'] = 1    # added the unknown token for laplace smoothing
    # totalBigrams += 1     # unknown token was added to vocabulary

    # print(tokenAppearance)

    return tokenAppearance, totalTrigrams




def createCorpus(directory, outputDir):
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
    return totalCorpus



def trigramSentenceProbability(trigramProbabilityInFile, bigramProbabilityInFile, unigramProbabilityInFile):

    probability = 0
    probabilitySum = 0
    sentences = []

    sentences.append('<start> this is the best thing ever ! <end>')
    sentences.append('<start> i am addicted to math . <end>')
    sentences.append('<start> fake news ... <end>')
    sentences.append('<start> Aabbcc hello abc <end>')


    for sentence in sentences:
        sentenceToCalc = sentence
        for word, nextWord, nextNext in zip(sentenceToCalc.split()[:-2], sentenceToCalc.split()[1:-1], sentenceToCalc.split()[2:]):
            if word.lower() + ' ' + nextWord.lower() + ' ' + nextNext.lower() not in trigramProbabilityInFile:
                # print('*****************************************************************')
                # print('Trigram: \'' + word.lower() + ' ' + nextWord.lower() + ' ' + nextNext.lower() + '\' is not in trigram dictionary. Calc as bigram')
                # print('*****************************************************************')

                if word.lower() + ' ' + nextWord.lower() not in bigramProbabilityInFile:
                    # print('*****************************************************************')
                    # print('Bigram: \'' + word.lower() + ' ' + nextWord.lower() + '\' is not in bigram dictionary. Calc as unigram')
                    # print('*****************************************************************')

                    if nextWord.lower() not in unigramProbabilityInFile:  # if also not in unigram - address as unknown
                        nextWord = '<unk>'
                    probability = unigramProbabilityInFile[nextWord.lower()]

                else:
                    probability = bigramProbabilityInFile[word.lower() + ' ' + nextWord.lower()]

            else:
                probability = trigramProbabilityInFile[word.lower() + ' ' + nextWord.lower() + ' ' + nextNext.lower()]


            if probabilitySum == 0:
                probabilitySum = probability
            else:
                probabilitySum *= probability

        print('\nSentence: \"' + sentence + '\" | probability is: ' + str(probabilitySum))




def bigramSentenceProbability(bigramProbabilityInFile, unigramProbabilityInFile):

    probability = 0
    probabilitySum = 0  # this will calculate the sum of the Log2 probabilities for the sentence
    sentences = []

    sentences.append('<start> when dogs fly . <end>')
    sentences.append('<start> Fake news ! <end>')
    sentences.append('<start> this is the best thing ever . <end>')
    sentences.append('<start> Aabbcc hello abc <end>')

    for sentence in sentences:
        sentenceToCalc = sentence
        for word, nextWord in zip(sentenceToCalc.split()[:-1], sentenceToCalc.split()[1:]):
            if word.lower() + ' ' + nextWord.lower() not in bigramProbabilityInFile:
                print('*****************************************************************')
                print('Bigram: \'' + word.lower() + ' ' + nextWord.lower() + '\' is not in bigram dictionary. Calc as unigram')
                print('*****************************************************************')

                if nextWord.lower() not in unigramProbabilityInFile:    # if also not in unigram - address as unknown
                    nextWord = '<unk>'
                probability = unigramProbabilityInFile[nextWord.lower()]

            else:
                probability = bigramProbabilityInFile[word.lower() + ' ' + nextWord.lower()]

            if probabilitySum == 0:
                probabilitySum = probability
            else:
                probabilitySum *= probability

        print('\nSentence: \"' + sentence + '\" | probability is: ' + str(probabilitySum))




def calcTokenProbabilityBigram(totalCorpus, unigramTotalAppearance):

    bigramAppearance, totalBigramsNum = createTokenAppearanceDictBigram(totalCorpus)  # return a token appearance dict, and the total number of words

    # for k in sorted(bigramProbabilityInFile, key=bigramProbabilityInFile.get, reverse=False):
    #     print(k, bigramProbabilityInFile[k])

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

    return bigramProbabilityInFile, bigramAppearance


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



def printRandomizedSentenceByDistribution(tokenProbabilityInFile, nGrams, secondaryProb={}):

    for i in range(3):
        sentence = createRandomizedSentenceByDistribution(tokenProbabilityInFile, nGrams, secondaryProb)
        for word in sentence:
            print(word + ' ', end='')
        print()


def createRandomizedSentenceByDistribution(tokenProbabilityInFile, nGrams, secondaryProb):
    sentence = []
    if nGrams == 'unigrams':
        print('in unigrams')
        word = ''
        while word != '<end>':
            word = randomWordByDistribution(tokenProbabilityInFile)
            sentence.append(word)

    elif nGrams == 'bigrams':
        # print('in bigrams')
        bigram = 't <start>'
        sentence.append('<start>')
        while bigram.split()[1] != '<end>':
            bigram = randomBigramByDistribution(tokenProbabilityInFile, bigram.split()[1])
            sentence.append(bigram.split()[1])


    elif nGrams == 'trigrams':
        # print('In trigrams')
        trigram = 't '
        bigram = 't <start>'
        bigram = randomBigramByDistribution(secondaryProb, bigram.split()[1])
        sentence.append('<start> ' + bigram.split()[1])
        trigram += bigram
        # print('trigram+bigram: ' + trigram)

        while trigram.split()[2] != '<end>':
            trigram = randomBigramByDistribution(tokenProbabilityInFile, trigram.split()[1] + ' ' + trigram.split()[2])
            sentence.append(trigram.split()[2])

    return sentence


def randomBigramByDistribution(tokenProbabilityInFile, lastWord):
    rand_val = random.random()
    total = 0
    newDict = {}

    for key in tokenProbabilityInFile:
        if key.startswith(lastWord):
            newDict[key] = tokenProbabilityInFile[key]

    values = list(newDict.values())
    valuesSum = sum(values)

    # normalize bigram distribution
    for key in newDict:
        newDict[key] = newDict[key] / valuesSum

    for k, v in newDict.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'


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


def unigramSentenceProbability(unigramProbabilityInFile):

    probabilitySum = 0  # this will calculate the sum of the Log2 probabilities for the sentence
    sentences = []

    sentences.append('I don \' t think so . . . <end>')
    sentences.append('Fake news ! <end>')
    sentences.append('There is no place like home . <end>')
    sentences.append('Aabbcc hello abc <end>')

    for sentence in sentences:
        sentenceToCalc = sentence.split()
        for word in sentenceToCalc:
            if word.lower() not in unigramProbabilityInFile:
                print('\n*****************************************************************')
                print('Word: \'' + word.lower() + '\' is not in dictionary. Changed to <unk>')
                print('*****************************************************************')
                word = '<unk>'
            if probabilitySum == 0:
                probabilitySum = unigramProbabilityInFile[word.lower()]
            else:
                probabilitySum *= unigramProbabilityInFile[word.lower()]
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
