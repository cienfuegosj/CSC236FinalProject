'''
Authors: Aleksandra Cvetanovska and Javier Cienfuegos
File: GUIApp.py
Description: This is the GUI application python file that has two implicit applications instantiated in.
Overall, this file allows us to define the settings for the two application objects used, mainly the tkinter object and
turtle window object. This file also includes all the game logic that will allow the windows to have the user interaction AND
the drawing logic. These are the following functions that were included from the cave backtracking assignment:

checkTreasure()
checkPos()
gamePlay()
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
    '''
    This class encapsulates all the logic and instantiation of the file dialog application.
    In this class, we create the graphical user interface, extract the filename that the user enters,
    read the file contents, and use a value-returning function to send the contents back to the main file
    '''

    def __init__(self, master):
        '''
        Constructor method for the FileApp object. This method will take in the parameter master, a tk a object,
        and create the graphical user interface.
        :param master:
        '''
        self.root = master
        self.f = None

        # Set the file name label text
        lbl_filename = StringVar()
        lbl_filename.set("Enter filename: ")

        emptyString = StringVar()
        emptyString.set("")

        # Instantiate a Frame object of tkinter class
        frame = Frame(master)
        frame.pack()

        # Create the file name label
        self.lbl_filename = Label(master, textvariable = lbl_filename, anchor = W, justify=LEFT)
        self.lbl_filename.pack()

        # Create the text box for the file name
        self.tbox_filename = Entry(master, textvariable = emptyString)
        self.tbox_filename.pack()

        # Create the button to initiate game
        self.btn_filesubmit = Button(master, justify=CENTER, text = "Submit", command = self.fileSubmitcallback)
        self.btn_filesubmit.pack()

    def fileSubmitcallback(self):
        '''
        Callback function for the __init__ method that will allow us to open the file which the user has provided.
        We try to open the file. If we do, we destroy the application, if not, we give an error.
        :return:
        '''

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
                self.root.destroy() # Destroy the application


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

class EditorApp:
    '''
    Editor Application class that allows us to encapsulate the tkinter object and intialize
    its properties and bindings. Most of the data retrieval is done here and the only
    external usage of this class is the getcolors method which gets the colors assigned
    by the user in the GUI.
    '''

    def __init__(self, master):

        tkMessageBox._show("Instructions", "Please select a color for each entry. List boxes"
                                           " do not keep their visual selection, but they are"
                                           " registered. Press Submit when finished.")

        self.root = master

        # Set the file name label text
        lbl_wallcolor = "Wall Color: "

        lbl_treasurecolor ="Treasure Color: "

        lbl_pathcolor = "Path Color: "

        lbl_traversecolor = "Traverse Color: "


        self.lbl_wallcolor = LabelFrame(master, text=lbl_wallcolor)
        self.lbl_wallcolor.pack()

        self.lbox_wallcolor = Listbox(self.lbl_wallcolor,selectmode=BROWSE,height=7)
        self.lbox_wallcolor.insert(1, "red")
        self.lbox_wallcolor.insert(2, "brown")
        self.lbox_wallcolor.insert(3, "purple")
        self.lbox_wallcolor.insert(4, "orange")
        self.lbox_wallcolor.insert(5, "yellow")
        self.lbox_wallcolor.insert(6, "green")
        self.lbox_wallcolor.insert(7, "white")

        self.lbl_treasurecolor = LabelFrame(master, text=lbl_treasurecolor)
        self.lbl_treasurecolor.pack()

        self.lbox_treasurecolor = Listbox(self.lbl_treasurecolor,selectmode=BROWSE,height=7)
        self.lbox_treasurecolor.insert(1, "red")
        self.lbox_treasurecolor.insert(2, "brown")
        self.lbox_treasurecolor.insert(3, "purple")
        self.lbox_treasurecolor.insert(4, "orange")
        self.lbox_treasurecolor.insert(5, "yellow")
        self.lbox_treasurecolor.insert(6, "green")
        self.lbox_treasurecolor.insert(7, "white")

        self.lbl_pathcolor = LabelFrame(master, text=lbl_pathcolor)
        self.lbl_pathcolor.pack()

        self.lbox_pathcolor = Listbox(self.lbl_pathcolor,selectmode=BROWSE,height=7)
        self.lbox_pathcolor.insert(1, "red")
        self.lbox_pathcolor.insert(2, "brown")
        self.lbox_pathcolor.insert(3, "purple")
        self.lbox_pathcolor.insert(4, "orange")
        self.lbox_pathcolor.insert(5, "yellow")
        self.lbox_pathcolor.insert(6, "green")
        self.lbox_pathcolor.insert(7, "white")

        self.lbl_traversecolor = LabelFrame(master, text=lbl_traversecolor)
        self.lbl_traversecolor.pack()

        self.lbox_traversecolor = Listbox(self.lbl_traversecolor,selectmode=BROWSE,height=7)
        self.lbox_traversecolor.insert(1, "red")
        self.lbox_traversecolor.insert(2, "brown")
        self.lbox_traversecolor.insert(3, "purple")
        self.lbox_traversecolor.insert(4, "orange")
        self.lbox_traversecolor.insert(5, "yellow")
        self.lbox_traversecolor.insert(6, "green")
        self.lbox_traversecolor.insert(7, "white")

        self.lbox_wallcolor.pack()
        self.lbox_treasurecolor.pack()
        self.lbox_pathcolor.pack()
        self.lbox_traversecolor.pack()

        self.btn_return = Button(self.lbl_traversecolor, justify=CENTER, text = "Submit", command = self.setcolors)
        self.btn_return.pack()

        self.lbox_wallcolor.bind('<ButtonRelease-1>', self.get_w)
        self.lbox_pathcolor.bind('<ButtonRelease-1>', self.get_p)
        self.lbox_treasurecolor.bind('<ButtonRelease-1>', self.get_t)
        self.lbox_traversecolor.bind('<ButtonRelease-1>', self.get_tr)

    def get_w(self, event):
        """
        Method to get the w entry in order to dedicate colors for the specific wall element
        of the matrix
        Note:
        W = Wall
        :return No return
        """

        windex = self.lbox_wallcolor.curselection()[0]
        self.lbox_wallcolor.activate(windex)
        self.wseltext = self.lbox_wallcolor.get(windex)
        tkMessageBox._show("Input Info.", "Wall color: " + str(self.wseltext))


    def get_t(self, event):
        '''
        Method to get the t entry in order to dedicate colors for the treasure element
        of the matrix.
        :param event: Binding event for the key press
        :return: No return
        '''

        tindex = self.lbox_treasurecolor.curselection()[0]
        self.lbox_treasurecolor.activate(tindex)
        self.tseltext = self.lbox_treasurecolor.get(tindex)
        tkMessageBox._show("Input Info.", "Treasure color: " + str(self.tseltext))


    def get_tr(self, event):
        '''
        Method to get the tr entry in order to dedicate colors for the traverse element
        of the matrix
        :param event: Binding event for the key press
        :return: No return
        '''

        trindex = self.lbox_traversecolor.curselection()[0]
        self.lbox_traversecolor.activate(trindex)
        self.trseltext = self.lbox_traversecolor.get(trindex)
        tkMessageBox._show("Input Info.", "Traverse color: " + str(self.trseltext))


    def get_p(self, event):
        '''
        Method to get the p entry in order to dedicate colors for the path element of the
        matrix
        :param event: Binding event for the key press
        :return: No return
        '''

        pindex = self.lbox_pathcolor.curselection()[0]
        self.lbox_pathcolor.activate(pindex)
        self.pseltext = self.lbox_pathcolor.get(pindex)
        tkMessageBox._show("Input Info.", "Path color: " + str(self.pseltext))


    def setcolors(self):
        '''
        Sets the colors of the entries and places them in a dictionary.
        :return: No return
        '''

        self.colors = {"W": self.wseltext, "T": self.tseltext, "M": "blue", ".": self.pseltext, "TR": self.trseltext}
        tkMessageBox._show("Redirect", "Processed! Please select OK.")
        self.root.destroy()

    def getcolors(self):
        '''
        Returns the value of the instance variable 'colors', which is a dictionary that maps out
        the colors to the corresponding matrix elements.
        :return: No return
        '''

        return self.colors

class MainApp:
    '''
    An application object that encapsulates all of the drawing functionalities and
    logic for the backtracking. We draw in this class and utilize the methods used
    in the backtracking cave assignment.
    '''

    def __init__(self, content, initialpos, colors):

        # Functionality Setup
        self.mappings = {} #Mappings of the points in (i,j) coordinates of the matrix to the actual canvas (x,y) coords
        self.currentState = pos() #Position object that lets us know about the current state
        self.nextState = pos() #Position object that lets us know about the next state
        self.treasures = {} #Treasure dictionary that maps out the treasure positions to the path stack
        self.stackObject = Stack() #Stack object that allows us to store our orientations (North, East, etc.)
        self.matrix = content #Two dimensional python list to store the rows and columns
        self.initialpos = initialpos #Position object that lets us know at what point in the matrix we have started
        self.colors = colors

        # Check if colors are not empty
        for item in self.colors:
            if self.colors[item] is None or self.colors[item] == "":
                self.colors = {"W": "red", "M": "blue", "T": "yellow", ".": "white", "TR": "blue"}
                break

        # Turtle Window GUI Setup
        self.row = len(content)
        self.col = len(content[0])
        self.canvaswidth = 1500
        self.canvasheight = 1500
        self.window = turtle.Screen()
        self.window.setup(width=self.canvaswidth,height=self.canvasheight)
        self.John = turtle.Turtle()
        self.John.speed(0)

        self.draw()
        self.window.exitonclick()


    def draw(self):

        #Determines what scaling factor to use relative to how many number of columns and rows we have.

        self.xscalingfactor = self.canvaswidth/self.col
        self.yscalingfactor = self.canvasheight/self.row
        self.xscalingfactor/=7
        self.yscalingfactor/=7

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
                    self.John.pen(fillcolor=self.colors["M"])
                    self.John.penup()
                    self.John.goto(self.currentState.col, self.currentState.row)
                    self.John.pendown()
                    self.John.begin_fill()
                    self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
                    self.John.end_fill()

                elif self.matrix[i][j] == "W":
                    self.mappings[(i, j)] = (self.currentState.col, self.currentState.row)
                    self.John.pen(fillcolor=self.colors["W"])
                    self.John.penup()
                    self.John.goto(self.currentState.col, self.currentState.row)
                    self.John.pendown()
                    self.John.begin_fill()
                    self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
                    self.John.end_fill()

                elif self.matrix[i][j] == "T":
                    self.mappings[(i, j)] = (self.currentState.col, self.currentState.row)
                    self.John.pen(fillcolor=self.colors["T"])
                    self.John.penup()
                    self.John.goto(self.currentState.col, self.currentState.row)
                    self.John.pendown()
                    self.John.begin_fill()
                    self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
                    self.John.end_fill()

                else:
                    self.mappings[(i, j)] = (self.currentState.col, self.currentState.row)
                    self.John.pen(fillcolor=self.colors["."])
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
        if self.matrix[self.nextState.row][self.nextState.col] ==  "T":
            x = copy.deepcopy(self.stackObject.items)
            position = pos(self.nextState.row, self.nextState.col)
            self.treasures[position] = x

    def checkPos(self):
        '''
        Checks the positions surrounding in order to find out where to go. We call this method our finding/logic method
        which determines where to go in our map. This method was used in the previous assignment: Cave Backtracking.
        Once we encounter a conditional in which our current position applies to, we draw a circle that is blue to
        represent that we have been there.
        :return:
        '''

        # North Conditional
        if self.matrix[self.currentState.row - 1][self.currentState.col] == "." and \
                        self.matrix[self.currentState.row - 1][self.currentState.col] != "B":
            self.stackObject.push(0)

            self.John.pen(fillcolor=self.colors['TR'])
            self.John.penup()
            self.John.goto(self.mappings[(self.currentState.row,self.currentState.col)][0],self.mappings[(self.currentState.row,self.currentState.col)][1])
            self.John.pendown()
            self.John.begin_fill()
            self.John.circle(math.sqrt(math.pow(self.xscalingfactor, 2) + math.pow(self.yscalingfactor, 2)))
            self.John.end_fill()

            self.currentState.row -= 1
            self.nextState.row = self.currentState.row - 1
            self.nextState.col = self.currentState.col

            self.John.pen(fillcolor=self.colors['TR'])
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

            self.John.pen(fillcolor=self.colors['TR'])
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

            self.John.pen(fillcolor=self.colors['TR'])
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

            self.John.pen(fillcolor=self.colors['TR'])
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

            self.John.pen(fillcolor=self.colors['TR'])
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

            self.John.pen(fillcolor=self.colors['TR'])
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

            self.John.pen(fillcolor=self.colors['TR'])
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
                    break
                else:
                    item = self.stackObject.pop()

                    # ---------Backtrack Process------------
                    # 0 represents that we went NORTH, so we need to go down, so row increase
                    # 1 represents that we went EAST, so we need to decrease the column
                    # 2 represent the we went SOUTH, so we need to row decrease
                    # 3 represent that we went WEST, so we need to increase the column
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



        tkMessageBox._show("Complete", "Congratulations!")
















