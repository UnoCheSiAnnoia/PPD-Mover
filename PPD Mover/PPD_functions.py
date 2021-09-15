import shutil
import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter import messagebox
from tkinter.constants import DISABLED
import zipfile
from tkinter import font
from PIL import ImageTk, Image


# variables
textDir = None
dirLines = []
songsDir = None
songsPath = None
startDir = None
textStartDir = None
zipPath = None
removeReadMe = None
removeZipFile = None
videoPath = None
selectedSongPath = None
vidStartingDir = None


def saves_finding_error():

    if os.path.exists(textDir.get()):
        return
    else:
        messagebox.showerror("File not found", "Saves file or folder not found\n Make sure there is a \"Saves\" folder with \"Saves_File.txt\" in it.")
        sys.exit()


def set_text_location():
    textDir.set(os.path.join(sys.path[0], "Saves", "Saves_File.txt"))
    saves_finding_error()


def file_read():
    saves_finding_error()
    textfile = open(textDir.get(), "r")
    global dirLines
    dirLines = textfile.readlines()
    textfile.close()


def append_to_empty():
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
    dirLines.append("Video starting folder:\n")
    dirLines.append("\n")
    textfile.writelines(dirLines)
    textfile.close()


def file_setup():
    file_read()
    global dirLines
    if not dirLines:
        append_to_empty()


def file_check():
    set_text_location()
    file_read()
    textfile = open(textDir.get(), "w")
    linecount = 0
    for _ in dirLines:
        linecount += 1

    def starting_append():
        dirLines.append("Starting folder:\n")
        dirLines.append("\n")

    def box1_append():
        dirLines.append("Box 1:\n")
        dirLines.append("Unchecked\n")

    def vid_starting_append():
        dirLines.append("Video starting folder:\n")
        dirLines.append("\n")

    if linecount == 0:
        file_setup()
    elif linecount == 1:
        dirLines.append("\n")
        starting_append()
        box1_append()
        vid_starting_append()
        textfile.writelines(dirLines)
    elif linecount == 2:
        starting_append()
        box1_append()
        vid_starting_append()
        textfile.writelines(dirLines)
    elif linecount == 3:
        dirLines.append("\n")
        box1_append()
        vid_starting_append()
        textfile.writelines(dirLines)
    elif linecount == 4:
        box1_append()
        vid_starting_append()
        textfile.writelines(dirLines)
    elif linecount == 5:
        dirLines.append("Unchecked\n")
        vid_starting_append()
        textfile.writelines(dirLines)
    elif linecount == 6:
        vid_starting_append()
        textfile.writelines(dirLines)
    elif linecount == 7:
        dirLines.append("\n")
        textfile.writelines(dirLines)
    if dirLines[0] != "PPD folder:\n":
        dirLines[0] = "PPD folder:\n"
    if dirLines[2] != "Starting folder:\n":
        dirLines[2] = "Starting folder:\n"
    if dirLines[4] != "Box 1:\n":
        dirLines[4] = "Box 1:\n"
    if dirLines[5] != "Unchecked\n" and dirLines[5] != "Checked\n":
        dirLines[5] = "Unchecked\n"
    if dirLines[6] != "Video starting folder:\n":
        dirLines[6] = "Video starting folder:\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()


def get_starting_dir_path():
    file_check()
    global dirLines
    songsPath.set(dirLines[1])


def get_songs_dir_path():
    selectedfolder = filedialog.askdirectory()
    songsPath.set(selectedfolder)
    print(songsPath.get())


def songs_dir_save():
    file_check()
    global dirLines
    global textDir
    textfile = open(textDir.get(), "w")
    dirLines[1] = songsPath.get() + "\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()


def read_start_from_file():
    file_check()
    global dirLines
    dirtouse = dirLines[3].rstrip("\n")
    if os.path.exists(dirtouse):
        textStartDir.set(dirtouse)
    elif dirtouse != "":
        messagebox.showwarning("Directory not found", "The starting directory could not be located.\nPlease set it up again")


def get_zip():
    read_start_from_file()
    selectedfile = filedialog.askopenfilename(initialdir=textStartDir.get(), filetypes=[("Zip files", "*.zip")])
    if selectedfile != "":
        zipPath.set(selectedfile)


def unzip():

    pathtoextract = songsPath.get().rstrip("\n")
    if os.path.exists(pathtoextract):
        tounzip = zipfile.ZipFile(zipPath.get().rstrip("\n"), mode="r")
        tounzip.extractall(path=pathtoextract)
    else:
        if pathtoextract == "":
            messagebox.showwarning("No location selected", "You have not selected a location to move the file to.\nPlease select it and try again")
        else:
            messagebox.showerror("Location not found", "the location you selected to move the zip file into was not found")


def move_file():
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


def save_starting_dir():
    file_check()
    global dirLines
    textfile = open(textDir.get(), "w")
    dirLines[3] = startDir.get() + "\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()


def get_starting_folder():
    selectedfolder = filedialog.askdirectory()
    startDir.set(selectedfolder)
    save_starting_dir()


def delete_saves():
    textfile = open(textDir.get(), "w")
    textfile.truncate(0)
    textfile.close()
    append_to_empty()


def check_remove_zip_initial():
    file_check()
    global dirLines
    if dirLines[5] == "Checked\n":
        removeZipFile.set(True)
    else:
        removeZipFile.set(False)


def check_remove_zip():
    file_check()
    global dirLines
    textfile = open(textDir.get(), "w")
    if removeZipFile.get():
        dirLines[5] = "Checked\n"
    else:
        dirLines[5] = "Unchecked\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()


def select_video():
    video = filedialog.askopenfilename(initialdir=vidStartingDir.get(), filetypes=[("MP4 files", "*.mp4")])
    if video != "":
        if os.path.exists(video):
            videoPath.set(video)
        else:
            messagebox.showerror("File not found", "the program was unable to find the video you selected")


def save_initial_vid_dir():
    file_check()
    global dirLines
    textfile = open(textDir.get(), "w")
    dirLines[7] = vidStartingDir.get() + "\n"
    textfile.truncate(0)
    textfile.writelines(dirLines)
    textfile.close()


def get_vid_dir():
    selectedfolder = filedialog.askdirectory()
    vidStartingDir.set(selectedfolder)
    save_initial_vid_dir()


def select_song():
    song = filedialog.askdirectory(initialdir=songsPath.get().rstrip("\n"))
    if song != "":
        if os.path.exists(song):
            selectedSongPath.set(song)
        else:
            messagebox.showerror("File not found", "The program was unable to find the selected folder")


def move_video():
    video = tk.StringVar()
    song = tk.StringVar()
    if videoPath.get() == "" and selectedSongPath.get() == "":
        messagebox.showwarning("no files selected", "Please select a video and the destination for the video")
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
    shutil.move(video.get(), os.path.join(song.get(), videoName))

