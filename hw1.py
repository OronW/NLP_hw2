import sys
import os
import csv
import re
from collections import defaultdict

# TODO: make path of directory an input by user before sending

directory = r'C:\Users\oron.werner\PycharmProjects\NLP\hw1Input'  # absolute path of folder
outputDir = r'C:\Users\oron.werner\PycharmProjects\NLP\hw1Output'  # absolute path of folder


def main(directory, numOfUsersToPrint, outputDir):  # directory=sys.argv[1], numOfUsers=sys.argv[2], outputDir=sys.argv[3]

    # directory = input()
    print()

    if not os.path.exists(outputDir):  # make output dir if not exists
        os.makedirs(outputDir)

    for currentFile in os.listdir(directory):
        if currentFile.endswith(".csv"):
            path = directory + '\\' + currentFile
            print(path)
            # file = open(path, 'r', encoding="utf8")
            # print(file)     # prints the name of file


            examineFile(path, numOfUsersToPrint, outputDir, currentFile)  # send the current file to work

            # TODO: change file name to name of user, after list is filled
            # f = open(outputDir + "\\" + currentFile[7:-18] + '.txt', 'w+')  # create a file with name of "file" .txt.  w+ is write privileges
            # break  # TODO: remove to go over all files. Currently only one file for testings

    # print("Total number of files in folder: " + str(os.listdir(directory).__len__()))  # prints number of files


def examineFile(filePath, numOfUsersToPrint, outputDir, currentFile):
    userList = createUserList(filePath)

    userSizeList = []

    # get posts by user as dictionary. KEY='user'
    postsByUser = getPosts(filePath, userList)

    # TODO: remove list bound for all users. This is just for testings
    for user in userList:
        currentUserPosts = postsByUser[user]  # this is an array with all the posts of one user
        userSentences = analyzePosts(currentUserPosts)

        # for sentence in userSentences:
        #     print(sentence.lstrip())
        postsByUser[user] = userSentences

        userSizeList.append([len(postsByUser[user]), user])

    usersByNumberOfSentences = sorted(userSizeList, reverse=True)

    createUsersFiles(numOfUsersToPrint, usersByNumberOfSentences, postsByUser, outputDir, currentFile)



def createUsersFiles(numOfUsersToPrint, usersByNumberOfSentences, postsByUser, outputDir, currentFile):


    for i in range(numOfUsersToPrint):
        print(usersByNumberOfSentences[i][1])
        f = open(outputDir + "\\" + usersByNumberOfSentences[i][1] + '_' + currentFile[7:-18] + '.txt', 'w+', encoding='utf-8')  # create a file with name of "file" .txt.  w+ is write privileges
        for post in postsByUser[usersByNumberOfSentences[i][1]]:
            f.write(post.lstrip()+'\n')
            # f.write('\n', encoding="utf-8")
            # print(post.lstrip())



def analyzePosts(userPosts):
    start = 0
    sentences = []  # this list will contain all the sentences of a user, derived from his/her posts

    # for post in userPosts:
    #     print(post)

    userPosts = cleanPosts(userPosts)
    sentences = makeSentences(userPosts)
    # sentences = tokenize(sentences)

    return sentences


def cleanPosts(userPosts):
    cleanedPosts = []

    for post in userPosts:
        currentPost = cleanLinks(post)  # if starts with a URL structure - delete the link
        # currentPost = cleansymbols(currentPost) # if there is any symbol - delete the "word" between left and right space

        cleanedPosts.append(currentPost)  # after all is cleaned - append to list

    return cleanedPosts


def cleanLinks(post):
    cleanedPost = ''
    splitPost = post.split()

    for i in splitPost:
        if 'http' not in i and \
                '@' not in i and \
                '#' not in i and \
                '^' not in i and \
                '*' not in i and \
                '&gt'not in i and \
                not i.startswith('['):
            cleanedPost = cleanedPost + ' ' + i

    return cleanedPost


def makeSentences(userPosts):
    sentences = []
    start = 0

    for post in userPosts:
        sentences.extend((re.findall('.*?[.?!]+|.+$', post)))     # this regex split the post by relevant characters, or by the end of the line


    return sentences


def getPosts(filePath, userList):
    with open(filePath, 'r', encoding="utf8") as csvFile:
        currentFile = csv.reader(csvFile, delimiter=',')

        postsByUser = {user: [] for user in userList}  # create a dictionary of posts by user. KEY='user'

        for row in currentFile:
            postsByUser[row[0]].append(row[3])

        print()
        print('*********************************')
        print()

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


main(directory, 3, outputDir)
