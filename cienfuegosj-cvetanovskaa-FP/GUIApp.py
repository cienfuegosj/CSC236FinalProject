'''
Authors: Javier Cienfuegos & Aleksandra Cvetanovska
File: GUIApp.py
Description: Tkinter objects will defined here
'''

from Tkinter import *
import tkMessageBox
import copy
import time
import pos

class FileApp:

    def __init__(self, master):

        self.root = master
        self.f = None

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
                self.f = open(filename, 'r')
            except IOError:
                tkMessageBox.showerror("Filename Error", "File could not open. Please try again.")
            else:
                tkMessageBox.showinfo("Filename Success", filename + " was successfully opened")
                time.sleep(1.5)
                self.root.destroy()


    def getfileContents(self):
        '''
        Returns the file contents in the form of a matrix in order to further parse the data.
        :return: A tuple that includes a two dimensional python list and the
        '''

        # -------------Extract the number of rows and columns from 'f_line'-----------
        f_line = self.f.readline()  # reads the first line
        list_f_line = f_line.split(" ")
        numRows = int(list_f_line[0])
        numCols = int(list_f_line[1])
        # ----------------------------------------------------------------------------


        # ----------------Extract the entire matrix into nested lists.----------------
        untrimmed_f_lines = self.f.read().splitlines()  # Untrimmed rows of characters, which include the whitespace characters
        trimmed_f_lines = []  # Trimmed rows of characters, which don't include the whitespace characters

        for line in untrimmed_f_lines:
            tmpstr = []
            for char in line:
                if char == " ":
                    continue
                else:
                    tmpstr.append(char)
            trimmed_f_lines.append(tmpstr)

        matrix = copy.deepcopy(trimmed_f_lines)  # Create a deep copy of the trimmed nested list for the matrix
        # ------------------------------------------------------------------------------


        # --------------Find where M is initially and store its position------------------
        # --------------Recall that indices start at 0, not 1-----------------------------

        for line in matrix:
            for char in line:
                if char == 'M':
                    initialpos = pos.pos(matrix.index(line), line.index(char))
                else:
                    continue
        # ------------------------------------------------------------------------------

        return (matrix, initialpos)

class MainApp:

    def __init__(self, master, content, initialpos):

        self.root = master
        self.content = content
        self.initialpos = initialpos

        self.window = PanedWindow(master, orient = VERTICAL,
                    bd=4,
                    borderwidth=4)
        self.window.pack(fill=BOTH, expand=1)

        self.mainpane = Canvas(self.window,
                        bg="white",
                        bd=3,
                        width=700,
                        height=400
                        )
        coord = 10, 50, 40, 80
        oval = self.mainpane.create_oval(coord, fill="blue")
        self.mainpane.pack(side=TOP)


        self.statisticspane = PanedWindow(self.window, orient=VERTICAL,
                            bg="grey",
                            bd=3,
                            borderwidth=4,
                            width=700,
                            height=100
                            )
        self.statisticspane.pack(side=BOTTOM)















