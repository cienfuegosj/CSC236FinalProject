'''
Authors: Javier Cienfuegos & Aleksandra Cvetanovska
File: GUIApp.py
Description: Tkinter objects will defined here
'''

from Tkinter import *
from pos import pos
from Stack import Stack
import tkMessageBox
import copy
import time


class FileApp:

    def __init__(self, master):

        self.root = master
        self.f = None

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
                    initialpos = pos(matrix.index(line), line.index(char))
                else:
                    continue
        # ------------------------------------------------------------------------------

        return (matrix, initialpos)

class MainApp:

    def __init__(self, master, content, initialpos):

        # Functionality Setup
        self.mappings = {}
        self.currentState = pos()
        self.nextState = pos()
        self.treasures = {}
        self.stackObject = Stack()
        self.matrix = content
        self.initialpos = initialpos

        # GUI Setup
        self.root = master
        self.canvaswidth = 700
        self.canvasheight = 400
        self.row = len(content)
        self.col = len(content[0])

        self.window = PanedWindow(master, orient = VERTICAL,
                    bd=4,
                    borderwidth=4)
        self.window.pack(fill=BOTH, expand=1)

        self.mainpane = Canvas(self.window,
                        bg="white",
                        bd=3,
                        width=self.canvaswidth,
                        height=self.canvasheight
                        )

        self.draw()
        self.mainpane.pack(side=TOP)



    def draw(self):

        xscalingfactor = self.canvaswidth/self.col-5
        yscalingfactor = self.canvasheight/self.row-5
        xscalingfactor/=2

        x1 = 10
        y1 = 10
        x2 = 10 + xscalingfactor
        y2 = 10 + yscalingfactor

        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] == "M":
                    self.mappings[(i,j)] = (x1,y1,x2,y2)
                    self.mainpane.create_oval(x1,y1,x2,y2, fill="blue", outline="blue")
                elif self.matrix[i][j] == "W":
                    self.mappings[(i, j)] = (x1, y1, x2, y2)
                    self.mainpane.create_rectangle(x1,y1,x2,y2, outline="red", fill="red")
                elif self.matrix[i][j] == "T":
                    self.mappings[(i, j)] = (x1, y1, x2, y2)
                    self.mainpane.create_rectangle(x1,y1,x2,y2, fill="#fff517", outline="#fff517")
                else:
                    self.mappings[(i, j)] = (x1, y1, x2, y2)
                    self.mainpane.create_oval(x1,y1,x2,y2, fill="white", outline="white")
                x1=x1+xscalingfactor+10
                x2=x2+xscalingfactor+10
            y1=y1+yscalingfactor+5
            y2=y2+yscalingfactor+5
            x1 = 10
            x2 = 10+xscalingfactor

        self.gamePlay()

    def checkTreasure(self):
        '''
        No pre conditions are made for this method.
        :return: notifies the user that we found treasure and we store the steps.
        '''

        if self.matrix[self.nextState.row][self.nextState.col] == "T":
            # If the next position is treasure then map it to the list of directions it took to get there
            tkMessageBox.showinfo("Treasure Info", "Treasure has been found!")
            x = copy.deepcopy(self.stackObject.items)
            position = pos(self.nextState.row, self.nextState.col)
            self.treasures[position] = x

    def checkPos(self):

        if self.matrix[self.currentState.row - 1][self.currentState.col] == "." and \
                        self.matrix[self.currentState.row - 1][self.currentState.col] != "B":
            self.stackObject.push(0)
            self.currentState.row -= 1
            self.nextState.row = self.currentState.row - 1
            self.nextState.col = self.currentState.col
            self.matrix[self.currentState.row][self.currentState.col] = "B"
            self.mainpane.create_oval(self.mappings[(self.currentState.row,self.currentState.col)][0],self.mappings[(self.currentState.row,self.currentState.col)][1],self.mappings[(self.currentState.row,self.currentState.col)][2],self.mappings[(self.currentState.row,self.currentState.col)][3], fill="blue")
            self.checkTreasure()
        elif self.matrix[self.currentState.row][self.currentState.col + 1] == "." and \
                        self.matrix[self.currentState.row][self.currentState.col + 1] != "B":
            self.stackObject.push(1)
            self.currentState.col = self.currentState.col + 1
            self.nextState.row = self.currentState.row
            self.nextState.col = self.currentState.col + 1
            self.matrix[self.currentState.row][self.currentState.col] = "B"
            self.mainpane.create_oval(self.mappings[(self.currentState.row,self.currentState.col)][0],self.mappings[(self.currentState.row,self.currentState.col)][1],self.mappings[(self.currentState.row,self.currentState.col)][2],self.mappings[(self.currentState.row,self.currentState.col)][3], fill="blue")
            self.checkTreasure()
        elif self.matrix[self.currentState.row][self.currentState.col - 1] == "." and \
                        self.matrix[self.currentState.row][self.currentState.col - 1] != "B":
            self.stackObject.push(3)
            self.currentState.col = self.currentState.col - 1
            self.nextState.row = self.currentState.row
            self.nextState.col = self.currentState.col - 1
            self.matrix[self.currentState.row][self.currentState.col] = "B"
            self.mainpane.create_oval(self.mappings[(self.currentState.row,self.currentState.col)][0],self.mappings[(self.currentState.row,self.currentState.col)][1],self.mappings[(self.currentState.row,self.currentState.col)][2],self.mappings[(self.currentState.row,self.currentState.col)][3], fill="blue")
            self.checkTreasure()
        elif self.matrix[self.currentState.row + 1][self.currentState.col] == '.' and \
                        self.matrix[self.currentState.row + 1][self.currentState.col] != "B":
            self.stackObject.push(2)
            self.nextState.row = self.currentState.row + 1
            self.nextState.col = self.currentState.col
            self.currentState.row = self.currentState.row + 1
            self.matrix[self.currentState.row][self.currentState.col] = "B"
            self.mainpane.create_oval(self.mappings[(self.currentState.row,self.currentState.col)][0],self.mappings[(self.currentState.row,self.currentState.col)][1],self.mappings[(self.currentState.row,self.currentState.col)][2],self.mappings[(self.currentState.row,self.currentState.col)][3], fill="blue")
            self.checkTreasure()
        else:
            return 0

    def gamePlay(self):
        '''
        :param initpos: Takes in the initial position as a position object.
        :return: Allows flow of the function as long as we are able to move throughout the map.
        '''

        self.currentState.col = self.initialpos.col
        self.currentState.row = self.initialpos.row

        while True:
            move = self.checkPos()
            if move == 0:  # Condition if there is no move.

                if self.stackObject.size() == 0:

                    print("Treasure Path List: ")
                    for key in list(self.treasures.keys()):
                        print(self.treasures[key])

                    print("That's all folks!")
                    break

                else:
                    item = self.stackObject.pop()

                    # ---------Backtrack Process------------
                    # 0 represents that we went NORTH, so we need to go down, so row increase
                    # 1 represents that we went EAST, so we need
                    if item == 0:
                        self.currentState.row += 1
                    elif item == 1:
                        self.currentState.col -= 1
                    elif item == 3:
                        self.currentState.col += 1
                    else:
                        self.currentState.row -= 1
            else:
                continue























