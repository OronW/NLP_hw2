import sys
import os
import csv
from collections import defaultdict


# TODO: make path of directory an input by user before sending

directory = r'C:\Users\oron.werner\PycharmProjects\NLP\hw1Input'    # absolute path of folder
outputDir = r'C:\Users\oron.werner\PycharmProjects\NLP\hw1Output'    # absolute path of folder



def main(directory, numOfUsers, outputDir):     # directory=sys.argv[1], numOfUsers=sys.argv[2], outputDir=sys.argv[3]


    # directory = input()
    print()

    if not os.path.exists(outputDir):   # make output dir if not exists
        os.makedirs(outputDir)

    for currentFile in os.listdir(directory):
        if currentFile.endswith(".csv"):
            path = directory + '\\' + currentFile
            print(path)
            # file = open(path, 'r', encoding="utf8")
            # print(file)     # prints the name of file

            examineFile(path)   # send the current file to work


            # TODO: change file name to name of user, after list is filled
            f = open(outputDir + "\\" + currentFile[:-4] + '.txt', 'w+')   # create a file with name of "file" .txt.  w+ is write privileges
            break   # TODO: remove to go over all files. Currently only one file for testings

    # print("Total number of files in folder: " + str(os.listdir(directory).__len__()))  # prints number of files



def examineFile(filePath):

    userList = createUserList(filePath)

    # get posts by user as dictionary. KEY='user'
    postsByUser = getPosts(filePath, userList)

    # TODO: remove list bound for all users. This is just for testings
    for user in userList[:1]:
        currentUserPosts = postsByUser[user]    # this is an array with all the posts of one user
        analyzePosts(currentUserPosts)

        print(currentUserPosts)



def analyzePosts(userPosts):

    start = 0
    sentences = []  # this list will contain all the sentences of a user, derived from his/her posts

    for post in userPosts:
        print(post)

    userPosts = cleanPosts(userPosts)
    sentences = makeSentences(userPosts)
    # sentences = tokenize(sentences)


    print()
    print('HERE')
    print()

    for sentence in sentences:
        print(sentence)
    pass


def cleanPosts(userPosts):
    cleanedPosts = []

    for post in userPosts:

        # currentPost = cleanLinks(post) # if starts with a URL structure - delete the link
        # currentPost = cleansymbols(currentPost) # if there is any symbol - delete the "word" between left and right space

        # cleanedPosts.append(currentPost)  # after all is cleaned - append to list

        if post.startswith('http'):
            x = slice(1, 3)
            cleanedPosts.append((post[x]))
        else:
            cleanedPosts.append(post)


    return cleanedPosts

def makeSentences(userPosts):
    sentences = []
    start = 0
    for post in userPosts:
        for i in range(0, len(post)):
            if post[i] == '.' or i == len(post)-1:
                sentences.append(post[start:i + 1])
                start = i + 1
        start = 0
    return sentences



def getPosts(filePath, userList):
    with open(filePath, 'r', encoding="utf8") as csvFile:
        currentFile = csv.reader(csvFile, delimiter=',')

        postsByUser = {user: [] for user in userList}   # create a dictionary of posts by user. KEY='user'

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