import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter.constants import DISABLED
import zipfile
from genericpath import isfile


#MAIN WINDOW SETTINGS
gui = tk.Tk()
gui.geometry("400x400")
gui.title("PPD mover")
gui.resizable(False,False)

#VARIABLES
textDir = tk.StringVar()
dirLines = []
songsDir = tk.StringVar()
songsPath = tk.StringVar()
startDir = tk.StringVar()
textStartDir = tk.StringVar()
zipPath = tk.StringVar()
removeReadMe = tk.BooleanVar()
removeZipFile = tk.BooleanVar()


#SAVES READING SETUP
def setTextLocation():
    textDir.set(os.path.join(sys.path[0], "Saves", "Saves_File.txt"))        #in future make a way to have a file even if someone changes the name of the file


#puts all the lines of the saves file in the dirLines list
def fileRead():
    textFile = open(textDir.get(), "r")
    global dirLines
    dirLines = textFile.readlines()
    textFile.close()


#setups the saves file. This is meant for an empty file.
def fileSetup():
    fileRead()
    global dirLines
    if(dirLines==[]):
        appendToEmpty()
        

def appendToEmpty():
    global dirLines
    dirLines = []
    directory = textDir.get()
    textFile = open(directory, "w")
    dirLines.append("PPD folder:\n")
    dirLines.append("\n")
    dirLines.append("Starting folder:\n")
    dirLines.append("\n")
    dirLines.append("Box 1:\n")
    dirLines.append("Unchecked\n")
    textFile.writelines(dirLines)
    textFile.close

#checks if the saves file is different from what it should be
def fileCheck():
    setTextLocation()
    fileRead()
    global dirLines
    textFile = open(textDir.get(), "w")
    linecount = 0
    #the number of lines is used later for checking if lines are missing
    for x in dirLines:
        linecount+=1
    
    #this functions are used to make the code below a bit shorter
    def startingAppend():
        dirLines.append("Starting folder:\n")
        dirLines.append("\n")
    def box1Append():
        dirLines.append("Box 1:\n")
        dirLines.append("Unchecked\n")

    #based on the linecount adds the missing line
    if(linecount == 0):
        fileSetup()
    elif(linecount < 2):
        dirLines.append("\n")
        startingAppend()
        box1Append()
        textFile.writelines(dirLines)
    elif(linecount < 3):
        startingAppend()
        box1Append()
        textFile.writelines(dirLines)
    elif(linecount < 4):
        dirLines.append("\n")
        box1Append()
        textFile.writelines(dirLines)
    elif(linecount < 5):
        box1Append()
        textFile.writelines(dirLines)
    elif(linecount < 6):
        dirLines.append("Unchecked\n")
        textFile.writelines(dirLines)

    #checks if all the lines have valid values
    if(dirLines[0] != "PPD folder:\n"):
        dirLines[0] = "PPD folder:\n"
    if(dirLines[2] != "Starting folder:\n"):
        dirLines[2] = "Starting folder:\n"
    if(dirLines[4] != "Box 1:\n"):
        dirLines[4] = "Box 1:\n"                                                                
    if(dirLines[5] != "Unchecked\n" and dirLines[5] != "Checked\n"):                            
        dirLines[5] = "Unchecked\n"                                                             
    textFile.truncate(0)
    textFile.writelines(dirLines)
    textFile.close()


#PPD SONGS FOLDER SELECTION
fileCheck()
songsDir.set(dirLines[1].rstrip("\n"))

def getStartingDirPath():
    fileCheck()
    global dirLines
    songsPath.set(dirLines[1])

def getSongsDirPath():
    selectedFolder = filedialog.askdirectory()
    if(selectedFolder != ""):
        songsPath.set(selectedFolder)

#the path should be in dirLines[1]
def songsDirSave():
    fileCheck()
    global dirLines
    global textDir
    textFile = open(textDir.get(), "w")
    dirLines[1] = songsPath.get() + "\n"
    textFile.truncate(0)
    textFile.writelines(dirLines)
    textFile.close()

#UI FOR SONGS SELECT
getStartingDirPath()

songsSelectLabel = tk.Label(gui, text="Select Directory")
songsSelectLabel.place(x=36,y=20)

songsSelectEntry = tk.Entry(gui, textvariable=songsPath, state=DISABLED)
songsSelectEntry.place(x=20,y=40)

songsFolderFind = tk.Button(gui, text="select", command=getSongsDirPath)
songsFolderFind.place(x=160,y=36)

songsFolderSave = tk.Button(gui, text="save folder", command=songsDirSave)
songsFolderSave.place(x=20,y=68)

#ZIP FILE SELECTION

#the starting directory for zip selection goes in dirLines[3]
def saveStartingDir():
    fileCheck()
    global dirLines
    textFile = open(textDir.get(), "w")
    dirLines[3] = startDir.get() + "\n"
    textFile.truncate(0)
    textFile.writelines(dirLines)
    textFile.close()

def getStartingFolder():
    selectedFolder = filedialog.askdirectory()
    startDir.set(selectedFolder)
    saveStartingDir()

def readStartFromFile():
    fileCheck()
    global dirLines
    dirToUse = dirLines[3].rstrip("\n")
    textStartDir.set(dirToUse)

def getZip():                                            
    readStartFromFile()                                  
    selectedFile = filedialog.askopenfilename(initialdir=textStartDir.get(), filetypes=[("Zip files", "*.zip")])
    if(selectedFile != ""):
        zipPath.set(selectedFile)

#uses split to get file name, puts it to unzip in the songs folder
def unzip():
    toUnzip = zipfile.ZipFile(zipPath.get().rstrip("\n"), mode="r")
    toUnzip.extractall(path = songsPath.get().rstrip("\n"))

def moveFile():
    zipFile = zipPath.get().rstrip("\n")
    if(os.path.exists(zipFile)):
        unzip()
        if(removeZipFile.get()):
            os.remove(zipPath.get().rstrip("\n"))


#UI FOR ZIP SELECT
zipSelectLabel = tk.Label(gui, text="Select .zip file")
zipSelectLabel.place(x=36,y=120)

zipSelectEntry = tk.Entry(gui, textvariable=zipPath, state=DISABLED)
zipSelectEntry.place(x=20,y=140)

zipFileFind = tk.Button(gui, text="Browse files", command=getZip)
zipFileFind.place(x=160,y=136)

moveFileButton = tk.Button(gui, text="Move", command=moveFile)
moveFileButton.place(x=20,y=168)

changeDirectory = tk.Button(gui, text="Change directory", command=getStartingFolder)
changeDirectory.place(x=80,y=168)


#SAVES DELETE BUTTON
def deleteSaves():
    textFile = open(textDir.get(), "w")
    textFile.truncate(0)
    textFile.close()
    appendToEmpty()

#SAVES DELETE BUTTON UI
deleteSavesButton = tk.Button(text = "delete saves", command=deleteSaves)
deleteSavesButton.place(x=20,y=252)

#REMOVE ZIP FILE
removeZipFile.set(False)

def checkRemoveZipInitial():
    fileCheck()
    global dirLines
    if(dirLines[5] == "Checked\n"):
        removeZipFile.set(True)
    else:
        removeZipFile.set(False)

def checkRemoveZip():
    fileCheck()
    global dirLines
    textFile = open(textDir.get(), "w")
    if(removeZipFile.get()):
        dirLines[5] = "Checked\n"
    else:
        dirLines[5] = "Unchecked\n"
    textFile.truncate(0)
    textFile.writelines(dirLines)
    textFile.close()

#REMOVE ZIP FILE UI
checkRemoveZipInitial()

removeZipBox = tk.Checkbutton(text = "remove .zip", variable=removeZipFile, command=checkRemoveZip, onvalue=True, offvalue=False)
removeZipBox.place(x=20,y=300)

#I still need to write the error handling code

gui.mainloop()


