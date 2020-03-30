import sys
import os
import csv


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



def examineFile(file):

    userList = createUserList(file)
    print('INSIDE')
    print(userList)

    pass





def createUserList(file):
    with open(file, 'r', encoding="utf8") as csvFile:
        currentFile = csv.reader(csvFile, delimiter=',')

        userList = []
        numOfUsers = 0
        currentUser = ""

        for row in currentFile:
            # print(currentUser)
            if row[0] != currentUser:
                numOfUsers += 1
                currentUser = row[0]
                userList.append(row[0])

    return userList


main(directory, 3, outputDir)