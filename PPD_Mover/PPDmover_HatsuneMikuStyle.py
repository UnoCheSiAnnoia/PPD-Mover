import PPD_functions as PPD
import tkinter as tk
import os
import sys
from tkinter.constants import DISABLED
from tkinter import font
from PIL import ImageTk, Image


def main():
    # main window setting
    gui = tk.Tk()
    gui.geometry("450x450")
    gui.configure(background="#4f5454")
    gui.title("PPD mover")
    gui.resizable(False, False)
    gui.iconbitmap(os.path.join(sys.path[0], "MIKUDAYO.ico"))

    # font setup
    Underlined = font.Font(gui, "TkDefaultFont")
    Underlined.configure(underline=True)

    # canvas setup
    canv = tk.Canvas(gui, width=450, height=450, bg="#4f5454", bd=0, highlightcolor="#4f5454",highlightbackground="#4f5454")
    Miku1 = Image.open(os.path.join(sys.path[0], "IMG", "Hatsune miku ppd 1.png"))
    MikuImage = ImageTk.PhotoImage(Miku1)
    backgroundMiku = canv.create_image(250, 250, image=MikuImage)
    selectDirOutline = canv.create_text(76, 28, text="Select Directory", font=Underlined, fill="#4b5676")
    selectDirText = canv.create_text(77, 29, text="Select Directory", font=Underlined, fill="White")
    selZipOutline = canv.create_text(76, 128, text="Select .zip file", font=Underlined, fill="#4b5676")
    selZipText = canv.create_text(77, 129, text="Select .zip file", font=Underlined, fill="White")
    selMp4Outline = canv.create_text(76, 228, text="Select the mp4", font=Underlined, fill="#4b5676")
    selMp4Text = canv.create_text(77, 229, text="Select the video", font=Underlined, fill="White")
    foldTextOutline = canv.create_text(252, 228, text="Select the song folder", font=Underlined, fill="#4b5676")
    selFoldText = canv.create_text(253, 229, text="Select the song folder", font=Underlined, fill="White")
    removeZipOutline = canv.create_text(65, 381, text="Delete .zip", fill="#4b5676")
    removeZipText = canv.create_text(64, 382, text="Delete .zip", fill="White")
    canv.place(x=0, y=0)

    PPD.textDir = tk.StringVar()
    PPD.songsDir = tk.StringVar()
    PPD.songsPath = tk.StringVar()
    PPD.startDir = tk.StringVar()
    PPD.textStartDir = tk.StringVar()
    PPD.zipPath = tk.StringVar()
    PPD.removeReadMe = tk.BooleanVar()
    PPD.removeZipFile = tk.BooleanVar()
    PPD.videoPath = tk.StringVar()
    PPD.selectedSongPath = tk.StringVar()
    PPD.vidStartingDir = tk.StringVar()

    # Song select UI

    PPD.get_starting_dir_path()

    songsSelectEntry = tk.Entry(gui, textvariable=PPD.songsPath, state=DISABLED, disabledbackground="#5a676b", disabledforeground="white")
    songsSelectEntry.place(x=15, y=40)

    songsFolderFind = tk.Button(gui, text="select", command=PPD.get_songs_dir_path, activebackground="#55d1d0",background="#87e5cf")
    songsFolderFind.place(x=16, y=68)

    songsFolderSave = tk.Button(gui, text="save folder", command=PPD.songs_dir_save, activebackground="#55d1d0",background="#87e5cf")
    songsFolderSave.place(x=160, y=36)

    # Zip select UI

    zipSelectEntry = tk.Entry(gui, textvariable=PPD.zipPath, state=DISABLED, disabledbackground="#5a676b",disabledforeground="white")
    zipSelectEntry.place(x=15, y=140)

    zipFileFind = tk.Button(gui, text="Browse files", command=PPD.get_zip, activebackground="#55d1d0", background="#87e5cf")
    zipFileFind.place(x=16, y=168)

    moveFileButton = tk.Button(gui, text="Move", command=PPD.move_file, activebackground="#55d1d0", background="#87e5cf")
    moveFileButton.place(x=160, y=136)

    changeDirectory = tk.Button(gui, text="Change directory", command=PPD.get_starting_folder, activebackground="#55d1d0",background="#87e5cf")
    changeDirectory.place(x=96, y=168)

    # Video select UI

    selectVideoEntry = tk.Entry(gui, state=DISABLED, textvariable=PPD.videoPath, disabledbackground="#5a676b",
                                disabledforeground="white")
    selectVideoEntry.place(x=15, y=240)

    selectSongEntry = tk.Entry(gui, state=DISABLED, textvariable=PPD.selectedSongPath, disabledbackground="#5a676b",
                               disabledforeground="white")
    selectSongEntry.place(x=190, y=240)

    selectVideoButton = tk.Button(text="Select", command=PPD.select_video, activebackground="#55d1d0", background="#87e5cf")
    selectVideoButton.place(x=16, y=268)

    selectStartingVideoDir = tk.Button(text="Change directory", command=PPD.get_vid_dir, activebackground="#55d1d0",
                                       background="#87e5cf")
    selectStartingVideoDir.place(x=65, y=268)

    selectSongButton = tk.Button(text="Select folder", command=PPD.select_song, activebackground="#55d1d0",
                                 background="#87e5cf")
    selectSongButton.place(x=190, y=268)

    moveVideoButton = tk.Button(text="Move video", command=PPD.move_video, activebackground="#55d1d0", background="#87e5cf")
    moveVideoButton.place(x=325, y=235)

    # Delete saves UI

    deleteSavesButton = tk.Button(text="delete saves", command=PPD.delete_saves, activebackground="#55d1d0", background="#87e5cf")
    deleteSavesButton.place(x=16, y=322)

    # Remove zip file checkbox UI

    PPD.check_remove_zip_initial()

    removeZipBox = tk.Checkbutton(variable=PPD.removeZipFile, command=PPD.check_remove_zip, onvalue=True, offvalue=False,
                                  background="#4f5454", activebackground="#4f5454", selectcolor="#5a676b", fg="White",
                                  activeforeground="White")
    removeZipBox.place(x=10, y=370)

    gui.mainloop()


if __name__ == "__main__":
    main()
