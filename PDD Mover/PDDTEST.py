#imports
from genericpath import isfile
from posixpath import splitext
import tkinter as tk
from tkinter import BooleanVar, ttk
from tkinter import filedialog
import shutil
import os
import sys
from tkinter.constants import X
import zipfile

#Main window setting
gui = tk.Tk()
gui.geometry("400x400")
gui.title("PDD Test")
gui.resizable(False,False)

#first setup for file reading:
#textDir: takes the Saves_File.txt in the PDD Mover folder (inside Saves folder)
#the other are just placeolders used for having a global variable
#i noticed now there is no real reason for textFile to be global but i don't think it matters
#so i'll just leave it like that
textDir = os.path.join(sys.path[0], "Saves", "Saves_File.txt")
textFile = "placeholder"
savedDir = ["placeholder"]

#what this does is that it opens the saves file saved in the textDir variable using the textFile variable
#to then put in savedDir the list of the lines of text in the file
def fileRead():
    global textDir 
    global textFile 
    textFile = open(textDir,"r")
    global savedDir
    savedDir = textFile.readlines()
    textFile.close()

#this function is necessary to setup the file if it is empty
def fileSetup():
    global savedDir
    global textDir
    textFile = open(textDir,"w")
    savedDir.append("PPD folder:\n")
    savedDir.append("\n")
    savedDir.append("Starting folder:\n")
    savedDir.append("\n")
    savedDir.append("Box 1:\n")
    savedDir.append("Unchecked\n")
    savedDir.append("Box 2:\n")
    savedDir.append("Unchecked\n")
    textFile.writelines(savedDir)
    textFile.close()

#This function should check the state of the file to see if something is missing or is not written correctly
#teoretically there shouldn't be the need for this but if someone modifies the saves file the whole thing might break.
#to make this thing work i use the linecount variable to see the number of lines, i put every missing lines in the text file with this function
#something that can happen is that i don't think this really checks what the lines say so it can still break i think, i need to fix this
def fileCheck():
    global linecount
    global savedDir
    global textDir
    textFile = open(textDir,"w")
    fileRead()
    for x in savedDir:
        linecount+=1
    if(linecount <1):
        fileSetup()
    elif(linecount <2):
        savedDir.append("\n")
        savedDir.append("Starting folder:\n")
        savedDir.append("\n")
        savedDir.append("Box 1:\n")
        savedDir.append("Unchecked\n")
        savedDir.append("Box 2:\n")
        savedDir.append("Unchecked\n")
        textFile.writelines(savedDir)
    elif(linecount <3):
        savedDir.append("Starting folder:\n")
        savedDir.append("\n")
        savedDir.append("Box 1:\n")
        savedDir.append("Unchecked\n")
        savedDir.append("Box 2:\n")
        savedDir.append("Unchecked\n")
        textFile.writelines(savedDir)
    elif(linecount <4):
        savedDir.append("\n")
        savedDir.append("Box 1:\n")
        savedDir.append("Unchecked\n")
        savedDir.append("Box 2:\n")
        savedDir.append("Unchecked\n")
        textFile.writelines(savedDir)
    elif(linecount <5):
        savedDir.append("Box 1:\n")
        savedDir.append("Unchecked\n")
        savedDir.append("Box 2:\n")
        savedDir.append("Unchecked\n")
        textFile.writelines(savedDir)
    elif(linecount <6):
        savedDir.append("Unchecked\n")
        savedDir.append("Box 2:\n")
        savedDir.append("Unchecked\n")
        textFile.writelines(savedDir)
    elif(linecount <7):
        savedDir.append("Box 2:\n")
        savedDir.append("Unchecked\n")
        textFile.writelines(savedDir)
    elif(linecount <8):
        savedDir.append("Unchecked\n")
        textFile.writelines(savedDir)
    #i am not sure if this part works correctly so i need to check it
    if(savedDir[0] != "PPD folder:\n"):
        savedDir[0] = "PPD folder:\n"
    if(savedDir[2] != "Starting folder:\n"):
        savedDir[2] = "Starting folder:\n"
    if(savedDir[4] != "Box 1:\n"):
        savedDir[4] == ""


#SELECTION OF THE DESTINATION FOLDER

fileRead()
#setup of the folderDirectory variable
folderDirectory = ""
#basically if the file is empty there is no folder directory saved, shocking uh? 
#probably this doesnt break if there is something strange in the line but when moving the file
#there will be an error i will have to handle, fun isn't it?
if(savedDir == []):
    folderDirectory = ""
    fileSetup()
else:
    folderDirectory = savedDir[1].rstrip("\n")

#this function makes you select from the classic selection menu a folder and puts the name in folderPath
#folderPath is a StringVar situated after this two functions (no need to comment this but I am lazy so...)
def getFolderPath(): 
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)

#ok found something to fix: since i should check the file before i won't need the first if right? I hope so because I'm gonna change it.
#anyways, this saves the folder selected in the file if i press the save folder button
def saveTheDirectory(): 
    global savedDir
    global textDir
    textFile = open(textDir,"w")
    if(savedDir == []):
        savedDir.append("PPD folder:\n")
        savedDir.append(folderPath.get()+"\n")
        savedDir.append("\n")
        savedDir.append("\n")
        savedDir.append("\n")
        savedDir.append("\n")
    else:
        savedDir[0] = "PPD folder:\n"
        savedDir[1] = folderPath.get() + "\n"
    textFile.truncate(0)
    textFile.writelines(savedDir)
    textFile.close()
        

#setup of the folderPath variable to the folderDirectory checked at the start of this section of code
folderPath = tk.StringVar()
folderPath.set(folderDirectory)
#text for the entry
dirSelectLabel = tk.Label(gui, text="Select Directory")
dirSelectLabel.grid(row=0,column=0)
#entry used to show the folder selected
dirSelectEntry = tk.Entry(gui,textvariable=folderPath)
dirSelectEntry.grid(row=0,column=1)
#button to change the folder inside the entry
#SIDE NOTE
#I am not really sure if this works correctly if i type the name of the folder instead of selecting it so i should check it
#(or disable somehow the possibility of writing in the entry and keep it just for the look)
btnFind = tk.Button(gui, text="Browse Folder", command=getFolderPath)
btnFind.grid(row=0,column=2)
#this saves the directory in the file
saveDirBtn = tk.Button(gui, text="Save Directory", command=saveTheDirectory)
saveDirBtn.grid(row=2,column=0)
 

 #SELECTION OF THE ZIP FILE CONTAINING THE SONG

#yeah the linecount variable is declared here. Any problems? this still works anyways
#but really, it is confusing if it is here tbh so i should change the position
linecount = 0
#some variables setup.
#this is used for starting in a certain directory (e.g. the download directory)
startDirectory = tk.StringVar()
startdir_fromtext = tk.StringVar()
#also here i can remove the part of code that setups the file, there should not be any need for it i can just call the check function
#anyways this changes the saved starting directory
def saveStartingDirectory():
    global savedDir
    textFile = open(textDir,"w")
    if(savedDir == []):
        savedDir.append("\n")
        savedDir.append("\n")
        savedDir.append("Starting Folder:\n")
        savedDir.append(startDirectory.get() + "\n")
        savedDir.append("\n")
        savedDir.append("\n")
    else:
        savedDir[2] = "Starting Folder:\n"
        savedDir[3] = startDirectory.get() + "\n"
    textFile.truncate(0)
    textFile.writelines(savedDir)
    textFile.close()
#this is used in the selection of the starting folder
def getStartingFolder():
    folder_selected = filedialog.askdirectory() 
    startDirectory.set(folder_selected)
    saveStartingDirectory()  

#the name gives it away, it reads from the file what directory to start in
def readFromFile():
    global savedDir
    if(savedDir == []):
        startdir_fromtext.set("")
    else:
        for x in savedDir:
            global linecount
            linecount+=1
        if(linecount >= 4):
            dirToUse = savedDir[3].rstrip("\n")
            startdir_fromtext.set(dirToUse)
        else:
            startdir_fromtext.set("")

#I don't understand how this function works and I don't know how I did make this
#I am pretty sure i didn't randomly get it from stackoverflow so i just forgot something i guess
def getZipPath():
    readFromFile()
    file_selected = filedialog.askopenfilename(initialdir=startdir_fromtext.get(), filetypes=[("Zip files", "*.zip")])
    zipPath.set(file_selected)

#gets the file position, unzips it, there is no more to say
def unzip():
    pathSplit = os.path.split(zipPath.get())
    zipName = pathSplit[1]
    unzipLocation = os.path.join(folderPath.get(), zipName)
    toUnzip = zipfile.ZipFile(unzipLocation, mode="r")
    toUnzip.extractall(path=folderPath.get())
    
#takes zipFile, moves it, if that box is checked removes an eventual readme (might be useful, idk)
#does the same thing of the readme also with the old zip file
def moveFile():
    zipFile = zipPath.get()
    Folder = folderPath.get()
    if(os.path.exists(zipFile)):
        shutil.move(zipFile, Folder)
        unzip()
        global removeReadmeVar
        if(removeReadmeVar.get() == True):
            removeReadMe()
        if(removeZip.get() == True):
            deleteZip()
    else:
        print("file not in directory or already moved")
        errorMessage.set("File not in directory or already moved")

#yeah actually it wasnt the thing above that removed the readme, that just called this function that actually does it
def removeReadMe():
    fileList = os.listdir(folderPath.get())
    for x in fileList:
        if (isfile(os.path.join(folderPath.get(),x))):
            if(x == "readme.txt"):
                os.remove(os.path.join(folderPath.get(),x))

#this deletes the old zip file
def deleteZip():
    pathSplit = os.path.split(zipPath.get())
    zipName = pathSplit[1]
    toDelete = os.path.join(folderPath.get(), zipName)
    os.remove(toDelete)


#code to execute the functions above
#the comment above was old but idk it is just funny so I am leaving it, I am probably rewrite this whole code so it doesn't matter lol
#setup for the variable
zipPath = tk.StringVar()
#label for the entry
zipSelectLabel = tk.Label(gui, text="Select .zip File")
zipSelectLabel.grid(row=6,column=0)
#entry
zipSelectEntry = tk.Entry(gui,textvariable=zipPath)
zipSelectEntry.grid(row=6,column=1)
#browse file to see what zip to move
btnFind2 = tk.Button(gui, text="Browse Files", command=getZipPath)
btnFind2.grid(row=6,column=2)

#button to execute the moving of the zip file
moveBtn = tk.Button(gui,text="Move", command=moveFile)
moveBtn.grid(row=10,column=0)
#this is for the starting folder, man this variable names really do suck ngl
changeDirBtn = tk.Button(gui,text="Change directory", command=getStartingFolder)
changeDirBtn.grid(row=12,column=0)

#checkbox delete readme.txt
#a probably overly complicated function to check the first checkbox
checkedFromFile = False
removeReadmeVar = tk.BooleanVar()


def checkBoxState():
    global savedDir
    global textDir
    global removeReadmeVar
    fileRead()
    textFile = open(textDir,"w")
    if(removeReadmeVar.get() == True):
        savedDir[4] = "Checkbox:\n"
        savedDir[5] = "Checked\n"
    else:
        savedDir[4] = "Checkbox:\n"
        savedDir[5] = "Unchecked\n"
    textFile.truncate(0)
    textFile.writelines(savedDir)
    textFile.close()

def checkBoxInitial():
    global savedDir
    global removeReadmeVar
    fileRead()
    if(savedDir[5].rstrip("\n") == "Checked"):
        removeReadmeVar.set(True)
    elif(savedDir[5].rstrip("\n") == "Unchecked"):
        removeReadmeVar.set(False)


        

checkBoxInitial()
removeReadmeBox = tk.Checkbutton(text="remove readme.txt",command=checkBoxState, variable=removeReadmeVar, onvalue=True, offvalue=False)
removeReadmeBox.grid(row=12,column=2)

#this button deletes all the saves (basically truncated the file to 0)

def deleteSaves():
    global textDir
    textFile = open(textDir, "w")
    textFile.truncate(0)
    textFile.close()


deleteSavesbtn = tk.Button(text="delete saves", command=deleteSaves)
deleteSavesbtn.grid(row=15 ,column=1 )




#does this actually work? I didn't even test it, i might as well comment this out but i won't. I am not even gonna comment this anymore because it isn't finished
removeZip = tk.BooleanVar()
removeZip.set(False)
def checkZipBoxInitial():
    global savedDir
    global removeZip
    fileRead()
    if(savedDir[7].rstrip("\n") == "Checked"):
        removeZip.set(True)
    elif(savedDir[7].rstrip("\n") == "Unchecked"):
        removeZip.set(False)

checkZipBoxInitial()

def saveZipBox():
    global savedDir
    global textDir
    global removeZip
    fileRead()
    if(removeZip.get() == True):
        savedDir[7] = "Checked\n"
    if(removeZip.get() == False):
        savedDir[7] = "Unchecked\n"

removeZipBox = tk.Checkbutton(text = "remove .zip",variable=removeZip,onvalue=True,offvalue=False,command=saveZipBox)
removeZipBox.grid(row=13, column=2)

#error message label setup
errorMessage = tk.StringVar()
error = tk.Label(gui, textvariable=errorMessage, fg="red")
error.grid(row=16, column=1)


#what i got from this is that i need to rewrite the whole code because it is a hot mess, I am gonna put this on github anyways because why not lol
gui.mainloop()