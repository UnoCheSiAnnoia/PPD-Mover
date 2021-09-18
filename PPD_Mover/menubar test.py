import tkinter as tk
from tkinter import Label, messagebox
root = tk.Tk()
root.geometry("450x450")
root.title = "Menubar test"
testLabel = tk.Label(text="Hello World!",font=("Courier", 40))
testLabel.pack()
testBool = tk.BooleanVar()
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
def Test1 ():
    messagebox.showinfo("TEST", "Zip cambiata!")
filemenu.add_command(label="Change .zip directory", command=Test1)
def Test2 ():
    messagebox.showinfo("TEST", "Video cambiato!")
filemenu.add_command(label="Change video directory", command=Test2)
filemenu.add_checkbutton(label="Delete .zip", onvalue=True, offvalue=False, variable=testBool)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
root.mainloop()