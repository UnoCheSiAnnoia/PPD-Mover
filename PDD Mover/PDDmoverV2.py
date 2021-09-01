import tkinter as tk
import os
import sys
from tkinter import filedialog
import zipfile
import shutil
from genericpath import isfile


#MAIN WINDOW SETTINGS
gui = tk.Tk()
gui.geometry = "400x400"
gui.title = "PPD Mover"
gui.resizable(False,False)

#VARIABLES
textDir = tk.StringVar()
dirLines = ["placeholder"]
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
    global dirLines
    directory = textDir.get()
    textFile = open(directory, "w")
    dirLines.append("PPD folder:\n")
    dirLines.append("\n")
    dirLines.append("Starting folder:\n")
    dirLines.append("\n")
    dirLines.append("Box 1:\n")
    dirLines.append("Unchecked\n")
    dirLines.append("Box 2:\n")
    dirLines.append("Unchecked")
    textFile.writelines(dirLines)
    textFile.close


#checks if the saves file is different from what it should be
def fileCheck():
    setTextLocation()
    global dirLines
    textFile = open(textDir.get(), "w")
    linecount = 0
    fileRead()
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
    def box2Append():
        dirLines.append("Box 2:\n")
        dirLines.append("Unchecked\n")

    #based on the linecount adds the missing line
    if(linecount == 0):
        fileSetup()
    elif(linecount < 2):
        dirLines.append("\n")
        startingAppend()
        box1Append()
        box2Append()
        textFile.writelines(dirLines)
    elif(linecount < 3):
        startingAppend()
        box1Append()
        box2Append()
        textFile.writelines(dirLines)
    elif(linecount < 4):
        dirLines.append("\n")
        box1Append()
        box2Append()
        textFile.writelines(dirLines)
    elif(linecount < 5):
        box1Append()
        box2Append()
        textFile.writelines(dirLines)
    elif(linecount < 6):
        dirLines.append("Unchecked\n")
        box2Append()
        textFile.writelines(dirLines)
    elif(linecount < 7):
        box2Append()
        textFile.writelines(dirLines)
    elif(linecount < 8):
        dirLines.append("Unchecked\n")
        textFile.writelines(dirLines)

    #checks if all the lines have valid values
    if(dirLines[0] != "PPD folder:\n"):
        dirLines[0] = "PPD folder:\n"
    if(dirLines[2] != "Starting folder:\n"):
        dirLines[2] = "Starting folder:\n"
    if(dirLines[4] != "Box 1:\n"):
        dirLines[4] = "Box 1:\n"                                                                #two things i could add if i wanted to:
    if(dirLines[5] != "Unchecked\n" and dirLines[5] != "Checked\n"):                            #-optimize this part of code a bit to not check every line
        dirLines[5] = "Checked\n"                                                               #this first thing isnt really that needed tbh so I'll think about it
    if(dirLines[6] != "Box 2:\n"):                                                              #-check the existance of the directory saved, I'll add this later
        dirLines[6] = "Box 2:\n"
    if(dirLines[7] != "Unchecked\n" and dirLines[7] != "Checked\n"):
        dirLines[7] = "Checked"
    textFile.truncate(0)
    textFile.writelines(dirLines)
    textFile.close()


#PPD SONGS FOLDER SELECTION
fileCheck()
songsDir = dirLines[1].rstrip("\n")

def getSongsDirPath():
    selectedFolder = filedialog.askdirectory()
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
songsSelectLabel = tk.Label(gui, text="Select Directory")
songsSelectLabel.grid(row=0,column=0)

songsSelectEntry = tk.Entry(gui, textvariable=songsPath)
songsSelectEntry.grid(row=0,column=0)

songsFolderFind = tk.Button

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

def getZip():                                            #I suddenly remembered how the code i wrote in the previous code worked
    readStartFromFile()                                  #So i can use it now, Yay!
    selectedFile = filedialog.askopenfilename(initialdir=textStartDir.get(), filetypes=[("Zip files", "*.zip")])
    zipPath.set(selectedFile)

#uses split to get file name, puts it to unzip in the songs folder
def unzip():
    pathSplit = os.path.split(zipPath.get())
    zipName = pathSplit[1]
    unzipLocation = os.path.join(songsPath.get(), zipName)
    toUnzip = zipfile.ZipFile(unzipLocation, mode="r")
    toUnzip.extractall(path = songsPath.get())

def moveFile():
    zipFile = zipPath.get()
    folder = songsPath.get()
    if(os.path.exists(zipFile)):
        shutil.move(zipFile, folder)
        unzip()
        if(removeReadMe.get()):
            deleteReadMe()
        if(removeZipFile.get()):
            pass

def deleteReadMe():
    fileList = os.listdir(songsPath.get())
    for x in fileList:
        if(isfile(os.path.join(songsPath.get(), x))):
            if(x == "readme.txt" or x == "ReadMe.txt" or x == "Readme.txt" or x == "README.txt"):
                os.remove(os.path.join(songsPath.get(), x))

def deleteZipFile():
    pathSplit = os.path.split(zipPath.get())
    zipName = pathSplit[1]
    toDelete = os.path.join(songsPath.get(), zipName)
    os.remove(toDelete)


#UI FOR ZIP SELECT
zipSelectLabel = tk.Label(gui, text="Select .zip file")
zipSelectLabel.grid(row=6, column=0)

zipSelectEntry = tk.Entry(gui, textvariable=zipPath)
zipSelectEntry.grid(row=6, column=1)

zipFileFind = tk.Button(gui, text="Browse files", command=getZip())
zipFileFind.grid(row=6, column=2)

moveFileButton = tk.Button(gui, text="Move", command=moveFile())
moveFileButton.grid(row=10, column=0)

changeDirectory = tk.Button(gui, text="Change directory", command=getStartingFolder())
changeDirectory.grid(row=12,column=0)


#REMOVE README CHECKBOX CODE
def checkRemoveReadme():
    global dirLines
    fileCheck()
    textFile = open(textDir.get(), "w")
    if(removeReadMe.get()):
        dirLines[5] = "Checked\n"
    else:
        dirLines[5] = "Unchecked\n"
    textFile.truncate(0)
    textFile.writelines(dirLines)
    textFile.close()

def checkRemoveReadmeInitial():
    global dirLines
    fileCheck()
    if(dirLines[5] == "Checked\n"):
        removeReadMe.set(True)
    else:
        removeReadMe.set(False)

#REMOVE README UI
checkRemoveReadmeInitial()
removeReadMeBox = tk.Checkbutton(text="remove readme.txt", command = checkRemoveReadme, variable=removeReadMe, onvalue=True, offvalue=False)
removeReadMeBox.grid(row=12, column=2)

#SAVES DELETE BUTTON
def deleteSaves():
    textFile = open(textDir.get(), "w")
    textFile.truncate(0)
    fileCheck()
    textFile.close()

#SAVES DELETE BUTTON UI
deleteSavesButton = tk.Button(text = "delete saves", command=deleteSaves)
deleteSavesButton.grid(row=15,column=1)

#REMOVE ZIP FILE
removeZipFile.set(False)

def checkRemoveZipInitial():
    global dirLines
    fileCheck()
    if(dirLines[7] == "Checked\n"):
        removeZipFile.set(True)
    else:
        removeZipFile.set(False)

def checkRemoveZip():
    global dirLines
    textFile = open(textDir.get(), "w")
    fileCheck()
    if(removeZipFile.get()):
        dirLines[7] = "Checked\n"
    else:
        dirLines[7] = "Unchecked\n"
    textFile.truncate(0)
    textFile.writelines(dirLines)
    textFile.close()

#REMOVE ZIP FILE UI
removeZipBox = tk.Checkbutton(text = "remove .zip", variable=removeZipFile, command=checkRemoveZip, onvalue=True, offvalue=False)
removeZipBox.grid(row=16, column=1)

#I still need to write the error handling code

gui.mainloop()


