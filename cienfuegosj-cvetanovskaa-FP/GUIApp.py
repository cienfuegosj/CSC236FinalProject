'''
Authors: Javier Cienfuegos & Aleksandra Cvetanovska
File: GUIApp.py
Description: Tkinter objects will defined here
'''

from Tkinter import *
import tkMessageBox

class FileApp:

    def __init__(self, master):

        '''StringVar objects defined here for labels'''

        lbl_filename = StringVar()
        lbl_filename.set("Enter filename: ")

        emptyString = StringVar()
        emptyString.set("")

        frame = Frame(master)
        frame.pack()

        self.lbl_filename = Label(master, textvariable = lbl_filename, anchor = W, justify=LEFT)
        self.lbl_filename.pack()

        self.tbox_filename = Entry(master, textvariable = emptyString)
        self.tbox_filename.pack()

        self.btn_filesubmit = Button(master, justify=CENTER, text = "Submit", command = self.fileSubmitcallback)
        self.btn_filesubmit.pack()

    def fileSubmitcallback(self):

        if self.tbox_filename.get() == "":
            tkMessageBox.showerror("Filename Error", "Please fill out the text field.")
        else:
            try:
                filename = "Cave Maps/" + self.tbox_filename.get()
                f = open(filename, 'r')
            except IOError:
                tkMessageBox.showerror("Filename Error", "File could not open. Please try again.")
            else:
                tkMessageBox.showinfo("Filename Success", filename + " was successfully opened")






