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
import turtle
import math

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

    def __init__(self, content, initialpos):

        # Functionality Setup
        self.mappings = {} #Mappings of the points in (i,j) coordinates of the matrix to the actual canvas (x,y) coords
        self.currentState = pos() #Position object that lets us know about the current state
        self.nextState = pos() #Position object that lets us know about the next state
        self.treasures = {} #Treasure dictionary that maps out the treasure positions to the path stack
        self.stackObject = Stack() #Stack object that allows us to store our orientations (North, East, etc.)
        self.matrix = content #Two dimensional python list to store the rows and columns
        self.initialpos = initialpos #Position object that lets us know at what point in the matrix we have started

        # Turtle Window GUI Setup
        self.row = len(content)
        self.col = len(content[0])
        self.canvaswidth = 700
        self.canvasheight = 400
        self.window = turtle.Screen()
        self.window.screensize(self.canvaswidth,self.canvasheight)
        self.John = turtle.Turtle()
        self.John.speed(0)
        self.draw()
        self.window.exitonclick()


    def draw(self):

        #Determines what scaling factor to use relative to how many number of columns and rows we have.

        self.xscalingfactor = self.canvaswidth/self.col
        self.yscalingfactor = self.canvasheight/self.row
        self.xscalingfactor/=2.8
        self.yscalingfactor/=2.8

        initialcanvasposx = -400
        initialcanvasposy = 300

        self.currentState.col = initialcanvasposx
        self.currentState.row = initialcanvasposy

        '''
        M represents where we have started
        W represents the walls which we are confined
        T represents a treasure object
        . represents our path
        '''

        colors = {"M":"blue", "W":"red", "T":"yellow", ".":"white"}

        '''
        The following code goes through the matrix, stores the (i,j) position and maps it to the actual coordinate position
        Then, a circle is drawn with a radius of R = sqrt(x^2 + y^2). The colors of the fill are determined by what letter is
        read from the matrix. We then move 2*R to the right in order to arrive at the next position of drawing. We then lower the
        y value by reducing the currentState's column value by 2*R and resetting the x value to the original x position on the canvas.
        '''

        for i in range(self.row):

            for j in range(self.col):

                if self.matrix[i][j] == "M":
                    self.mappings[(i,j)] = (self.currentState.col, self.currentState.row)
                    self.John.pen(fillcolor=colors["M"])
                    self.John.penup()
                    self.John.goto(self.currentState.col, self.currentState.row)
                    self.John.pendown()
                    self.John.begin_fill()
                    self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
                    self.John.end_fill()

                elif self.matrix[i][j] == "W":
                    self.mappings[(i, j)] = (self.currentState.col, self.currentState.row)
                    self.John.pen(fillcolor=colors["W"])
                    self.John.penup()
                    self.John.goto(self.currentState.col, self.currentState.row)
                    self.John.pendown()
                    self.John.begin_fill()
                    self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
                    self.John.end_fill()

                elif self.matrix[i][j] == "T":
                    self.mappings[(i, j)] = (self.currentState.col, self.currentState.row)
                    self.John.pen(fillcolor=colors["T"])
                    self.John.penup()
                    self.John.goto(self.currentState.col, self.currentState.row)
                    self.John.pendown()
                    self.John.begin_fill()
                    self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
                    self.John.end_fill()

                else:
                    self.mappings[(i, j)] = (self.currentState.col, self.currentState.row)
                    self.John.pen(fillcolor=colors["."])
                    self.John.penup()
                    self.John.goto(self.currentState.col, self.currentState.row)
                    self.John.pendown()
                    self.John.begin_fill()
                    self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
                    self.John.end_fill()

                self.currentState.col += 2*math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2))

            self.currentState.col = initialcanvasposx
            self.currentState.row -= 2*math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2))

        self.gamePlay()

    def checkTreasure(self):
        '''
        No pre conditions are made for this method.
        :return: notifies the user that we found treasure and we store the steps.
        '''
        if self.matrix[self.nextState.row][self.nextState.col] == "T":
            x = copy.deepcopy(self.stackObject.items)
            position = pos(self.nextState.row, self.nextState.col)
            self.treasures[position] = x

    def checkPos(self):

        # North Conditional
        if self.matrix[self.currentState.row - 1][self.currentState.col] == "." and \
                        self.matrix[self.currentState.row - 1][self.currentState.col] != "B":
            self.stackObject.push(0)

            self.John.pen(fillcolor="blue")
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row,self.currentState.col)][0],self.mappings[(self.currentState.row,self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.currentState.row -= 1
            self.nextState.row = self.currentState.row - 1
            self.nextState.col = self.currentState.col

            self.John.pen(fillcolor="blue")
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row, self.currentState.col)][0],
                           self.mappings[(self.currentState.row, self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.matrix[self.currentState.row][self.currentState.col] = "B"
            self.checkTreasure()
        # EAST Conditional
        elif self.matrix[self.currentState.row][self.currentState.col + 1] == "." and \
                        self.matrix[self.currentState.row][self.currentState.col + 1] != "B":
            self.stackObject.push(1)

            self.John.pen(fillcolor="blue")
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row, self.currentState.col)][0],
                           self.mappings[(self.currentState.row, self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.currentState.col = self.currentState.col + 1
            self.nextState.row = self.currentState.row
            self.nextState.col = self.currentState.col + 1

            self.John.pen(fillcolor="blue")
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row, self.currentState.col)][0],
                           self.mappings[(self.currentState.row, self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.matrix[self.currentState.row][self.currentState.col] = "B"
            self.checkTreasure()
        # West Conditional
        elif self.matrix[self.currentState.row][self.currentState.col - 1] == "." and \
                        self.matrix[self.currentState.row][self.currentState.col - 1] != "B":
            self.stackObject.push(3)

            self.John.pen(fillcolor="blue")
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row, self.currentState.col)][0],
                           self.mappings[(self.currentState.row, self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.currentState.col = self.currentState.col - 1
            self.nextState.row = self.currentState.row
            self.nextState.col = self.currentState.col - 1

            self.John.pen(fillcolor="blue")
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row, self.currentState.col)][0],
                           self.mappings[(self.currentState.row, self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.matrix[self.currentState.row][self.currentState.col] = "B"
            self.checkTreasure()
        # South Conditional
        elif self.matrix[self.currentState.row + 1][self.currentState.col] == '.' and \
                        self.matrix[self.currentState.row + 1][self.currentState.col] != "B":
            self.stackObject.push(2)

            self.John.pen(fillcolor="blue")
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row, self.currentState.col)][0],
                           self.mappings[(self.currentState.row, self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.currentState.row = self.currentState.row + 1
            self.nextState.row = self.currentState.row + 1
            self.nextState.col = self.currentState.col

            self.John.pen(fillcolor="blue")
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row, self.currentState.col)][0],
                           self.mappings[(self.currentState.row, self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.matrix[self.currentState.row][self.currentState.col] = "B"

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
                    for key in list(self.treasures.keys()):
                        print(self.treasures[key])
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

        tkMessageBox._show("Complete", "Congratulations!\nTreasure Found: " + str(len(self.treasures)))
















