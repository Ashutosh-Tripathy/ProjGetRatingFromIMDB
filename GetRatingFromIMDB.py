import logging
import requests
import os
import bs4
import sys
from os import rename, listdir
from bs4 import BeautifulSoup

logger = logging.getLogger('your-module')
logger.setLevel(logging.DEBUG)
undoChanges = False

# # Initialize coloredlogs.
# import coloredlogs
# coloredlogs.install(level='DEBUG')


def GetFolderPath():
    user_input = input("Enter the path of your folder: ")
    assert os.path.exists(
        user_input), "I did not find the folder at: " + str(user_input)
    # return 'C:\\Personal\\Intel related'
    return user_input


def GetVideoFormat():
    return {'.avi', '.mp4', '.mov', '.mkv', '.flv'}


def IsVideoFile(filename):
    # logger.critical('Fileextension: '+os.path.splitext(filename)[1])
    if(os.path.splitext(filename)[1] in videorFormats):
        logger.error('Video file: ' + filename)
        return True
    else:
        # logger.error('Not a video file: '+filename)
        return False


def ChageFileNameIntoSearchableFormat(filename):
    space = ' '
    separator = ['.', '_', '-', ' ', '[', ']', '(', ')']
    for sep in separator:
        if(filename.count(sep) > 4):
            return space.join(filename.split(sep)[0:5])
        else:
            filename = filename.replace(sep, space)
    return filename


def GetGoogleResponseForIMDBRating(fullFilename):
    filename = os.path.splitext(fullFilename)[0]
    filename = ChageFileNameIntoSearchableFormat(filename)
    url = 'https://google.com/search?q=' + filename + " imdb"
    print("URL: " + url)
    res = requests.get(url)
    res = BeautifulSoup(res.text, "html.parser")
    # text_file = open("Output.txt", "w")
    # text_file.write("Purchase Amount: %s" % res.encode('ascii', 'ignore'))
    # text_file.close()
    # print("GetGoogleResponseForIMDBRating"+str(res.encode('ascii', 'ignore')))
    return res


def GetAllResultFromGoogleResponse(googleResponse):
    googleTopResults = googleResponse.find_all(class_="g", limit=3)
    if(len(googleTopResults) > 0):
        return googleTopResults
    else:
        return ""


def GetRating(tagContent):
    try:
        index = tagContent.index("/10")
        rating = tagContent[index - 3:index]
        rating = rating.replace(':', '').replace(' ', '')
        print("Rating: " + rating)
        return rating
    except:
        print("No rating found")
        return -1


def GetRatingDivFirstResult(allResult):
    for temp in allResult:
        tag = temp.find_all('div', class_="slp")
    # print("Tag: "+str(tag))
        if(len(tag) > 0):
            rating = GetRating(str(tag))
            if(rating != -1):
                return rating
    else:
        return -1


def DisplayResult(filename, rating):
    # print("-------------------------------------")
    if(rating == -1):
        print("No rating found for file: " + filename)
    elif(rating == -2):
        print("File already proecessed: " + filename)
    else:
        print("Rating for file " + filename + " is: " + rating)


def GetIMDBRatingFromGoogleSearch(fullFilename):
    googleResponse = GetGoogleResponseForIMDBRating(fullFilename)
    googleTopResults = GetAllResultFromGoogleResponse(googleResponse)
    if(googleTopResults != ""):
        return GetRatingDivFirstResult(googleTopResults)
    else:
        # logger.warn("No result from google for serarch query")
        return -1
    # print("Google response: "+ str(googleResponse));


def FileAlreadyProcessedPreviously(fullFilename):
    return "==" in os.path.splitext(fullFilename)[0][-7:]


def AppendRatingInVideoFileNameAndReturnNewName(folderName, fullFilename, rating):
    newName = os.path.splitext(fullFilename)[
        0] + "==" + rating + os.path.splitext(fullFilename)[1]
    print("Renamed file " + fullFilename + " to " + newName)
    os.rename(os.path.join(folderName, fullFilename),
              os.path.join(folderName, newName))
    return newName


def GetNewFileNameAfterAppendingRating(folderName, fullFilename, rating):
    if float(rating) > 0:
        return AppendRatingInVideoFileNameAndReturnNewName(folderName, fullFilename, rating)
    else:
        return ""

def UndoFileNameChanges(folderName, fullFilename):
    fileName = os.path.splitext(fullFilename)[0]
    originalName = fileName[:fileName.index("==")] + os.path.splitext(fullFilename)[1]
    os.rename(os.path.join(folderName, fullFilename),
              os.path.join(folderName, originalName))

def StartProcessOfGettingRatingFromIMDBAndReturnNewName(folderName, fullFilename):
    if undoChanges:
        rating = -2
        if FileAlreadyProcessedPreviously(fullFilename):
            UndoFileNameChanges(folderName, fullFilename)
            print("Undoing changes.")
    elif FileAlreadyProcessedPreviously(fullFilename):
        print(fullFilename + " already processed.")
        rating = -2
    else:
        rating= GetIMDBRatingFromGoogleSearch(fullFilename)
        DisplayResult(fullFilename,rating)
    return GetNewFileNameAfterAppendingRating(folderName, fullFilename, rating)


def TraverseFolderAndAddRatingInVideFiles(folderPath):
    for folderName, subfolders, filenames in os.walk(folderPath):
        print('======================================================================')
        print('Current  folder  is  ' + folderName)
        for fullFilename in filenames:
            if(IsVideoFile(fullFilename)):
                renamedFullFilename = StartProcessOfGettingRatingFromIMDBAndReturnNewName(
                    folderName, fullFilename)
                print("             --------------")


folderPath = GetFolderPath()
videorFormats = GetVideoFormat()
TraverseFolderAndAddRatingInVideFiles(folderPath)
