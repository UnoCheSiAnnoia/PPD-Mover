import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter import messagebox
from tkinter.constants import DISABLED
import zipfile
from tkinter import font
from PIL import ImageTk, Image

# MAIN WINDOW SETTINGS
gui = tk.Tk()
gui.geometry("450x450")
gui.configure(background="#4f5454")
gui.title("PPD mover")
gui.resizable(False, False)

Underlined = font.Font(gui, "TkDefaultFont")
Underlined.configure(underline=True)

# canvas setup
canv = tk.Canvas(gui, width=450, height=450, bg="#4f5454", bd=0, highlightcolor="#4f5454", highlightbackground="#4f5454")
Miku1 = Image.open(os.path.join(sys.path[0], "IMG", "Hatsune miku ppd 1.png"))
MikuImage = ImageTk.PhotoImage(Miku1)
backgroundMiku = canv.create_image(250, 250, image=MikuImage)
selectDirOutline = canv.create_text(76, 28, text="Select Directory", font=Underlined, fill="#4b5676")
selectDirText = canv.create_text(77, 29, text="Select Directory", font=Underlined, fill="White")
selZipOutline = canv.create_text(76, 128, text="Select .zip file", font=Underlined, fill="#4b5676")
selZipText = canv.create_text(77, 129, text="Select .zip file", font=Underlined, fill="White")
selMp4Outline = canv.create_text(76, 228, text="Select the mp4", font=Underlined, fill="#4b5676")
selMp4Text = canv.create_text(77, 229, text="Select the mp4", font=Underlined, fill="White")
foldTextOutline = canv.create_text(252, 228, text="Select the song folder", font=Underlined, fill="#4b5676")
selFoldText = canv.create_text(253, 229, text="Select the song folder", font=Underlined, fill="White")
removeZipOutline = canv.create_text(65, 381, text="Delete .zip", fill="#4b5676")
removeZipText = canv.create_text(64, 382, text="Delete .zip", fill="White")


canv.place(x=0, y=0)

# VARIABLES
textDir = tk.StringVar()
dirLines = []
songsDir = tk.StringVar()
songsPath = tk.StringVar()
startDir = tk.StringVar()
textStartDir = tk.StringVar()
zipPath = tk.StringVar()
removeReadMe = tk.BooleanVar()
removeZipFile = tk.BooleanVar()
videoPath = tk.StringVar()
selectedSongPath = tk.StringVar()

# SAVES READING SETUP


def settextlocation():
    textDir.set(os.path.join(sys.path[0], "Saves", "Saves_File.txt"))
    # in future make a way to have a file even if someone changes the name of the file
    savesfindingerror()


# puts all the lines of the saves file in the dirLines list
def fileread():
    savesfindingerror()
    textfile = open(textDir.get(), "r")
    global dirLines
    dirLines = textfile.readlines()
    textfile.close()


def savesfindingerror():
    if os.path.exists(textDir.get()):
        return
    else:
        messagebox.showerror("File not found", "the program was unable to locate the saves folder, make sure it is "
                                               "located into a folder called \"Saves\" and that the file is called "
                                               "\"Saves_File.txt\", then restart the program")
        gui.destroy()


# setups the saves file. This is meant for an empty file.
def filesetup():
    fileread()
    global dirLines
    if not dirLines:
        appendtoempty()


def appendtoempty():
    global dirLines
    dirLines = []
    directory = textDir.get()
    textfile = open(directory, "w")
    dirLines.append("PPD folder:\n")
    dirLines.append("\n")
    dirLines.append("Starting folder:\n")
    dirLines.append("\n")
    dirLines.append("Box 1:\n")
    dirLines.append("Unchecked\n")
    textfile.writelines(dirLines)
    textfile.close()

# checks if the saves file is different from what it should be


def filecheck():
    settextlocation()
    fileread()
    global dirLines
    textfile = open(textDir.get(), "w")
    linecount = 0
    # the number of lines is used later for checking if lines are missing
    for _ in dirLines:
        linecount += 1

    # this functions are used to make the code below a bit shorter
    def startingappend():
        dirLines.append("Starting folder:\n")
        dirLines.append("\n")

    def box1append():
        dirLines.append("Box 1:\n")
        dirLines.append("Unchecked\n")

    # based on the linecount adds the missing line
    if linecount == 0:
        filesetup()
    elif linecount < 2:
        dirLines.append("\n")
        startingappend()
        box1append()
        textfile.writelines(dirLines)
    elif linecount < 3:
        startingappend()
        box1append()
        textfile.writelines(dirLines)
    elif linecount < 4:
        dirLines.append("\n")
        box1append()
        textfile.writelines(dirLines)
    elif linecount < 5:
        box1append()
        textfile.writelines(dirLines)
    elif linecount < 6:
        dirLines.append("Unchecked\n")
        textfile.writelines(dirLines)

    # checks if all the lines have valid values
    if dirLines[0] != "PPD folder:\n":
        dirLines[0] = "PPD folder:\n"
    if dirLines[2] != "Starting folder:\n":
        dirLines[2] = "Starting folder:\n"
    if dirLines[4] != "Box 1:\n":
        dirLines[4] = "Box 1:\n"
    if dirLines[5] != "Unchecked\n" and dirLines[5] != "Checked\n":
        dirLines[5] = "Unchecked\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()


# PPD SONGS FOLDER SELECTION
filecheck()
songsDir.set(dirLines[1].rstrip("\n"))


def getstartingdirpath():
    filecheck()
    global dirLines
    songsPath.set(dirLines[1])


def getsongsdirpath():
    selectedfolder = filedialog.askdirectory()
    if selectedfolder != "":
        songsPath.set(selectedfolder)

# the path should be in dirLines[1]


def songsdirsave():
    filecheck()
    global dirLines
    global textDir
    textfile = open(textDir.get(), "w")
    dirLines[1] = songsPath.get() + "\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()

# UI FOR SONGS SELECT


getstartingdirpath()

songsSelectEntry = tk.Entry(gui, textvariable=songsPath, state=DISABLED, disabledbackground="#5a676b", disabledforeground="white")
songsSelectEntry.place(x=15, y=40)

songsFolderFind = tk.Button(gui, text="select", command=getsongsdirpath, activebackground="#55d1d0", background="#87e5cf")
songsFolderFind.place(x=16, y=68)

songsFolderSave = tk.Button(gui, text="save folder", command=songsdirsave, activebackground="#55d1d0", background="#87e5cf")
songsFolderSave.place(x=160, y=36)

# ZIP FILE SELECTION

# the starting directory for zip selection goes in dirLines[3]


def savestartingdir():
    filecheck()
    global dirLines
    textfile = open(textDir.get(), "w")
    dirLines[3] = startDir.get() + "\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()


def getstartingfolder():
    selectedfolder = filedialog.askdirectory()
    startDir.set(selectedfolder)
    savestartingdir()


def readstartfromfile():
    filecheck()
    global dirLines
    dirtouse = dirLines[3].rstrip("\n")
    if os.path.exists(dirtouse):
        textStartDir.set(dirtouse)
    elif dirtouse != "":
        messagebox.showwarning("Directory not found", "the starting directory you set up was not found, if you are sure"
                                                      " the directory exists, try to select it once more")


def getzip():
    readstartfromfile()
    selectedfile = filedialog.askopenfilename(initialdir=textStartDir.get(), filetypes=[("Zip files", "*.zip")])
    if selectedfile != "":
        zipPath.set(selectedfile)

# uses split to get file name, puts it to unzip in the songs folder


def unzip():

    pathtoextract = songsPath.get().rstrip("\n")
    if os.path.exists(pathtoextract):
        tounzip = zipfile.ZipFile(zipPath.get().rstrip("\n"), mode="r")
        tounzip.extractall(path=pathtoextract)
    else:
        if pathtoextract == "":
            messagebox.showwarning("No location selected", "You haven't selected a directory to move the zip file to, p"
                                                           "lease select one and try again")
        else:
            messagebox.showerror("Location not found", "the location you selected to move the zip file into was not found")


def movefile():
    filezip = zipPath.get().rstrip("\n")
    if os.path.exists(filezip):
        unzip()
        if removeZipFile.get():
            os.remove(zipPath.get().rstrip("\n"))
    else:
        if filezip == "":
            messagebox.showwarning("No file selected", "You have not selected a zip file, please select one and try again")
        else:
            messagebox.showerror("Zip file not found", "the selected zip file was not found by the program")


# UI FOR ZIP SELECT


zipSelectEntry = tk.Entry(gui, textvariable=zipPath, state=DISABLED, disabledbackground="#5a676b", disabledforeground="white")
zipSelectEntry.place(x=15, y=140)

zipFileFind = tk.Button(gui, text="Browse files", command=getzip, activebackground="#55d1d0", background="#87e5cf")
zipFileFind.place(x=16, y=168)  # 16, 168

moveFileButton = tk.Button(gui, text="Move", command=movefile, activebackground="#55d1d0", background="#87e5cf")
moveFileButton.place(x=160, y=136)  # 160, 136

changeDirectory = tk.Button(gui, text="Change directory", command=getstartingfolder, activebackground="#55d1d0", background="#87e5cf")
changeDirectory.place(x=96, y=168)


# SAVES DELETE BUTTON
def deletesaves():
    textfile = open(textDir.get(), "w")
    textfile.truncate(0)
    textfile.close()
    appendtoempty()

# SAVES DELETE BUTTON UI


deleteSavesButton = tk.Button(text="delete saves", command=deletesaves, activebackground="#55d1d0", background="#87e5cf")
deleteSavesButton.place(x=16, y=322)

# REMOVE ZIP FILE
removeZipFile.set(False)


def checkremovezipinitial():
    filecheck()
    global dirLines
    if dirLines[5] == "Checked\n":
        removeZipFile.set(True)
    else:
        removeZipFile.set(False)


def checkremovezip():
    filecheck()
    global dirLines
    textfile = open(textDir.get(), "w")
    if removeZipFile.get():
        dirLines[5] = "Checked\n"
    else:
        dirLines[5] = "Unchecked\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()

# REMOVE ZIP FILE UI


checkremovezipinitial()

removeZipBox = tk.Checkbutton(variable=removeZipFile, command=checkremovezip, onvalue=True, offvalue=False, background="#4f5454", activebackground="#4f5454", selectcolor="#5a676b", fg="White", activeforeground="White")
removeZipBox.place(x=10, y=370)

# VIDEO SELECT

# selectVideoButton code


def selectvideo():
    video = filedialog.askopenfilename()
    if video != "":
        if os.path.exists(video):
            videoPath.set(video)
        else:
            messagebox.showerror("File not found", "the program was unable to find the video you selected")

# selectSongButton code


def selectsong():
    song = filedialog.askdirectory(initialdir=songsPath.get().rstrip("\n"))
    if song != "":
        if os.path.exists(song):
            selectedSongPath.set(song)
        else:
            messagebox.showerror("File not found", "The program was unable to find the selected folder")

# moveVideoButton code


def movevideo():
    video = tk.StringVar()
    song = tk.StringVar()
    if videoPath.get() == "" and selectedSongPath.get() == "":
        messagebox.showwarning("no files selected", "you need to select a video and the destination for the video before proceeding")
        return
    else:
        if videoPath.get() == "":
            messagebox.showwarning("no file selected", "please select the video you want to move")
            return
        else:
            if os.path.exists(videoPath.get()):
                video.set(videoPath.get())
            else:
                messagebox.showerror("no video found", "the program was unable to find the selected video")
                return
        if selectedSongPath.get() == "":
            messagebox.showwarning("no file selected", "please select the folder where you want to put the video")
            return
        else:
            if os.path.exists(selectedSongPath.get()):
                song.set(selectedSongPath.get())
            else:
                messagebox.showerror("folder not found", "the program was unable to find the folder")
    pathSplit = os.path.split(video.get())
    videoName = pathSplit[1]
    os.replace(video.get(), os.path.join(song.get(), videoName))


# UI FOR THE VIDEO SELECT


selectVideoEntry = tk.Entry(gui, state=DISABLED, textvariable=videoPath, disabledbackground="#5a676b", disabledforeground="white")
selectVideoEntry.place(x=15, y=240)

selectSongEntry = tk.Entry(gui, state=DISABLED, textvariable=selectedSongPath, disabledbackground="#5a676b", disabledforeground="white")
selectSongEntry.place(x=190, y=240)

selectVideoButton = tk.Button(text="Select", command=selectvideo, activebackground="#55d1d0", background="#87e5cf")
selectVideoButton.place(x=16, y=268)

selectStartingVideoDir = tk.Button(text="Change directory", activebackground="#55d1d0", background="#87e5cf")
selectStartingVideoDir.place(x=65, y=268)

selectSongButton = tk.Button(text="Select folder", command=selectsong, activebackground="#55d1d0", background="#87e5cf")
selectSongButton.place(x=190, y=268)

moveVideoButton = tk.Button(text="Move video", command=movevideo, activebackground="#55d1d0", background="#87e5cf")
moveVideoButton.place(x=325, y=235)

gui.mainloop()
