import math
import sys
import os
import csv
import re
from collections import defaultdict

# input files directory: C:\Users\oron.werner\PycharmProjects\NLP\hw1Input
directory = r'C:\Users\oron.werner\PycharmProjects\NLP\hw1Input'
outputDir = r'C:\Users\oron.werner\PycharmProjects\NLP\hw2Output'
numOfUsers = 10


def main():  # directory=sys.argv[1], numOfUsers=sys.argv[2], outputDir=sys.argv[3]
    print('*********************************')
    numOfUsersToPrint = int(numOfUsers)
    totalCorpus = []

    if not os.path.exists(outputDir):  # make output dir if not exists
        os.makedirs(outputDir)

    for currentFile in os.listdir(directory):
        if currentFile.endswith(".csv"):
            path = directory + '\\' + currentFile
            print()
            print('Reading the file: ')
            print(path)

            corpus = examineFile(path, numOfUsersToPrint, outputDir, currentFile)  # send the current file to work
            totalCorpus += corpus

        print('*********************************')

    # TODO: remove file creation before sending. For testing purpose only
    f = open(outputDir + "\\" + 'test' + '.txt', 'w+', encoding='utf-8')   # creates a file with all users for testings
    for line in totalCorpus:
        f.write(line)
        f.write('\n')


    calcTokenProbability(totalCorpus)



def examineFile(filePath, numOfUsersToPrint, outputDir, currentFile):
    userList = createUserList(filePath)

    userSizeList = []
    corpus = []

    # get posts by user as dictionary. KEY='user'
    postsByUser = getPosts(filePath, userList)

    for user in userList:
        currentUserPosts = postsByUser[user]  # this is an array with all the posts of one user
        userSentences = analyzePosts(currentUserPosts)
        postsByUser[user] = userSentences
        userSizeList.append([len(postsByUser[user]), user])

    usersByNumberOfSentences = sorted(userSizeList, reverse=True)

    corpus = createCorpus(numOfUsersToPrint, usersByNumberOfSentences, postsByUser, outputDir, currentFile)
    # createUsersFiles(numOfUsersToPrint, usersByNumberOfSentences, postsByUser, outputDir, currentFile)

    return corpus


def calcTokenProbability(totalCorpus):

    tokenAppearance, totalWords = createTokenAppearanceDict(totalCorpus)  # return a token appearance dict, and the total number of words

    # for k in sorted(tokenAppearance, key=tokenAppearance.get, reverse=True):
    #     print(k, tokenAppearance[k])

    vocabularySize = len(tokenAppearance)
    print('Len of dic is: ' + str(len(tokenAppearance)))
    print('Total number of words: ' + str(totalWords))

    tokenProbabilityInFile = tokenAppearance.copy()

    for token in tokenProbabilityInFile:
        tokenProbabilityInFile[token] = math.log10(tokenAppearance[token]/(totalWords + vocabularySize))
    # reconstructedTokenCount
#     TODO: Check if should work with log
#     for k in sorted(tokenProbabilityInFile, key=tokenProbabilityInFile.get, reverse=False):
#         print(k, tokenProbabilityInFile[k])

    calcSentenceProbability(tokenProbabilityInFile)


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
                print('\nWord: ' + word.lower() + ' ,not in dictionary. Changed to <unk>\n')
                word = '<unk>'
            probabilitySum += tokenProbabilityInFile[word.lower()]
        print('\nSentence: \"' + sentence + '\" probability is: ' + str(math.exp(probabilitySum)))



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


def createCorpus(numOfUsersToPrint, usersByNumberOfSentences, postsByUser, outputDir, currentFile):

    corpus = []

    print()
    print('Top ' + str(numOfUsersToPrint) + ' users for this file are: ')
    print('------------------------------')

    for i in range(numOfUsersToPrint):
        print(usersByNumberOfSentences[i][1])
        for post in postsByUser[usersByNumberOfSentences[i][1]]:
            corpus.append(post.lstrip() + ' ' + '<end>')

    return corpus
    # print(corpus)
    # f = open(outputDir + "\\" + 'test' + '_' + currentFile[7:-18] + '.txt', 'w+', encoding='utf-8')   #   creates a file with all users for testings
    # for line in corpus:
    #     f.write(line + '\n')


def createUsersFiles(numOfUsersToPrint, usersByNumberOfSentences, postsByUser, outputDir, currentFile):
    print()
    print('Top ' + str(numOfUsersToPrint) + ' users for this file are: ')
    print('------------------------------')

    f = open(outputDir + "\\" + 'TopUsers' + '_' + currentFile[7:-18] + '.txt', 'w+', encoding='utf-8')  # create a file with name of "file" .txt.  w+ is write privileges
    for i in range(numOfUsersToPrint):
        print(usersByNumberOfSentences[i][1])
        for post in postsByUser[usersByNumberOfSentences[i][1]]:
            f.write(post.lstrip() + ' ' + '<end>' + '\n')

    print()
    print('Files written to:')
    print(outputDir)
    print()


def analyzePosts(userPosts):
    sentences = []  # this list will contain all the sentences of a user, derived from his/her posts

    userPosts = cleanPosts(userPosts)
    sentences = makeSentences(userPosts)
    for sentence in sentences:
        re.sub('\s\s+', ' ', sentence)
    sentences = tokenize(sentences)

    return sentences


def tokenize(tempSentences):
    sentences = []
    for sentence in tempSentences:
        sentences.append(re.sub('(?<=[.,"\'!?:’])(?=[^\s])|(?=[.,"\'!?:’])(?<=[^\s])', ' ', sentence))

    return sentences


def cleanPosts(userPosts):
    cleanedPosts = []

    for post in userPosts:
        currentPost = cleanLinks(post)  # if starts with a URL structure - delete the link
        cleanedPosts.append(currentPost)  # after all is cleaned - append to list

    return cleanedPosts


def cleanLinks(post):
    cleanedPost = ''
    splitPost = re.split('\s|;', post)

    # list of rules to clean
    regex = [re.compile('^(http|www)')]
    regex.append(re.compile('[^\w_\'.?!’]'))

    dontAddPostFlag = False

    for i in splitPost:
        for j in range(len(regex)):
            if regex[j].search(i):
                dontAddPostFlag = True

        if dontAddPostFlag is False:
            cleanedPost = cleanedPost + ' ' + i

        dontAddPostFlag = False

    return cleanedPost


def makeSentences(userPosts):
    sentences = []

    for post in userPosts:
        sentences.extend((re.findall('.*?[.?!]+[msMS]?\.?|.+[^\s]', post)))     # this regex split the post by relevant characters, or by the end of the line | working old: '.*?[.?!]+|.+$'

    return sentences


def getPosts(filePath, userList):
    with open(filePath, 'r', encoding="utf8") as csvFile:
        currentFile = csv.reader(csvFile, delimiter=',')

        postsByUser = {user: [] for user in userList}  # create a dictionary of posts by user. KEY='user'

        for row in currentFile:
            postsByUser[row[0]].append(row[3])

    return postsByUser


def createUserList(filePath):
    with open(filePath, 'r', encoding="utf8") as csvFile:
        currentFile = csv.reader(csvFile, delimiter=',')

        userList = []
        currentUser = ""

        for row in currentFile:
            if row[0] != currentUser:
                currentUser = row[0]
                userList.append(row[0])

    return userList


main()
