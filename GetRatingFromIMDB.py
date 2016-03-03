import logging, requests, os, bs4, sys
from os import rename, listdir
from bs4 import BeautifulSoup
logger = logging.getLogger('your-module')
logger.setLevel(logging.DEBUG)
# # Initialize coloredlogs.
# import coloredlogs
# coloredlogs.install(level='DEBUG')

def GetFolderPath():
    return 'C:\\Personal\\Intel related'
    
def GetVideoFormat():
    return {'.avi','.mp4','.mov','.mkv'}
    
def IsVideoFile(filename):
    # logger.critical('Fileextension: '+os.path.splitext(filename)[1])
    if(os.path.splitext(filename)[1] in videorFormats):
        logger.error('Video file: '+filename)
        return True
    else:
        # logger.error('Not a video file: '+filename)
        return False

def GetGoogleResponseForIMDBRating(fullFilename):
    url='https://google.com/search?q='+os.path.splitext(fullFilename)[0]+" imdb"
    print("URL: "+url)
    res= requests.get(url)
    res= BeautifulSoup(res.text,"html.parser")
    # text_file = open("Output.txt", "a")
    # text_file.write("Purchase Amount: %s" % res.encode('ascii', 'ignore'))
    # text_file.close()
    # print("GetGoogleResponseForIMDBRating"+str(res.encode('ascii', 'ignore')))
    return res
    
def GetFristResultFromGoogleResponse(googleResponse):
    googleFirstResult=googleResponse.find_all(class_="g",limit=1)
    if(len(googleFirstResult)>0):
        firstElemnt= googleFirstResult[0]
        # for tag in firstElemnt:
        #     print (tag.name)
        return firstElemnt
    else:
        # logger.warn("No result from google for search request")
        return ""

def GetRating(tagContent):    
        try:
            index=tagContent.index("/10");
            rating=tagContent[index-3:index]
            print("GetRating Rating: "+rating)
            return rating
        except:
            print("No rating found")    
            return -1

def GetRatingDivFirstResult(firstResult):
    # for tag in firstResult:
    #     print(tag.name)
    tag= firstResult.find_all('div',class_="slp")
    # print("Tag: "+str(tag))
    if(len(tag)>0):
        return  GetRating(str(tag))
    else:
        return -1;
        
def DisplayResult(filename,rating):
    # print("-------------------------------------")
    if(rating==-1):
        print("No rating found for file: "+filename)
    elif(rating==-2):
        print("File already proecessed: "+filename)
    else:
        print("Rating for file " +filename+" is: "+rating)
        
def GetIMDBRatingFromGoogleSearch(fullFilename):
    googleResponse=GetGoogleResponseForIMDBRating(fullFilename)
    firstResult=GetFristResultFromGoogleResponse(googleResponse)
    if(firstResult!=""):
        return GetRatingDivFirstResult(firstResult)
    else:
        # logger.warn("No result from google for serarch query")
        return -1
    # print("Google response: "+ str(googleResponse));

def FileAlreadyProcessedPreviously(fullFilename):
    try:
        os.path.splitext(fullFilename)[0][-6:].index("-")
        return True
    except:
        return False           

def AppendRatingInVideoFileNameAndReturnNewName(folderName,fullFilename,rating):
    newName=os.path.splitext(fullFilename)[0]+"-"+rating+os.path.splitext(fullFilename)[1]
    print("Renamed file "+fullFilename+" to "+newName)
    os.rename(os.path.join(folderName, fullFilename), os.path.join(folderName, newName))
    return newName

def GetNewFileNameAfterAppendingRating(folderName,fullFilename,rating):
    if(float(rating)>0):
        return AppendRatingInVideoFileNameAndReturnNewName(folderName,fullFilename,rating)
    else:
        return ""
    
def StartProcessOfGettingRatingFromIMDBAndReturnNewName(folderName,fullFilename):
    if(FileAlreadyProcessedPreviously(fullFilename)):
        rating=-2
    else:
        rating= GetIMDBRatingFromGoogleSearch(fullFilename)
        DisplayResult(fullFilename,rating)
    return    GetNewFileNameAfterAppendingRating(folderName,fullFilename,rating)     
         
def TraverseFolderAndAddRatingInVideFiles(folderPath):
    for	folderName,	subfolders,	filenames	in	os.walk(folderPath):
        print('======================================================================')
        print('Current	folder	is	'	+	folderName)
        for	fullFilename	in	filenames:            
            if(IsVideoFile(fullFilename)):
                renamedFullFilename=StartProcessOfGettingRatingFromIMDBAndReturnNewName(folderName,fullFilename) 
                print("             --------------")
                    
user_input = input("Enter the path of your folder: ")
assert os.path.exists(user_input), "I did not find the folder at: "+str(user_input)
folderPath=GetFolderPath()
videorFormats=GetVideoFormat()
TraverseFolderAndAddRatingInVideFiles(folderPath)
    

