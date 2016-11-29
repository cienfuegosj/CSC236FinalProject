import copy
from Stack import Stack
from pos import pos

class Game(object):
    
    def __init__(self):
        ''' 
           The initializer function. It creates all of the game's objects.
        '''
        #NORTH = 0
        #EAST = 1
        #WEST = 2
        #SOUTH = 3
        
        self.numRows = None
        self.numCols = None
        self.currentState = pos() #An object of pos() class which stores the current position
        self.nextState = pos() #An object of pos() class which stores the next position we'll be at
        self.matrix = [] # A matrix which stores our map
        self.treasures = {} # A dictionary which maps the treasure's position to the list of directions it takes to get there
        self.stackObject = Stack() # A stack object used to store the directions we've gone through
    
    def GameInit(self, f):
        '''

        :param f: f is the file object passed in through the driver file.
        :return: Creates the matrix and finds the initial position.
        '''
    
        #-------------Extract the number of rows and columns from 'f_line'-----------
        f_line = f.readline() #reads the first line
        list_f_line = f_line.split(" ")
        self.numRows = int(list_f_line[0])
        self.numCols = int(list_f_line[1])
        #----------------------------------------------------------------------------
        
        
        #----------------Extract the entire matrix into nested lists.----------------
        untrimmed_f_lines = f.read().splitlines() # Untrimmed rows of characters, which include the whitespace characters
        trimmed_f_lines = [] # Trimmed rows of characters, which don't include the whitespace characters
        
        for line in untrimmed_f_lines:
            tmpstr = []
            for char in line:
                if char == " ":
                    continue
                else:
                    tmpstr.append(char)
            trimmed_f_lines.append(tmpstr)
            
        self.matrix = copy.deepcopy(trimmed_f_lines) # Create a deep copy of the trimmed nested list for the matrix
        #------------------------------------------------------------------------------
        
        
        #--------------Find where M is initially and store its position------------------
        #--------------Recall that indices start at 0, not 1-----------------------------
        
        for line in self.matrix:
            for char in line:
                if char == 'M':
                    initialpos = pos(self.matrix.index(line),line.index(char))
                else:
                    continue
        #------------------------------------------------------------------------------
     
        #self.gamePlayAlpha(initialpos) # Start actually moving
        self.gamePlay(initialpos)
        
    def checkTreasure(self):
        '''
        No pre conditions are made for this method.
        :return: notifies the user that we found treasure and we store the steps.
        '''
        
        if self.matrix[self.nextState.row][self.nextState.col]=="T":
        #If the next position is treasure then map it to the list of directions it took to get there
            print("YAAAAS TREASURE")
            x = copy.deepcopy(self.stackObject.items)
            position = pos(self.nextState.row, self.nextState.col)
            self.treasures[position] = x
            

    def checkPos(self,initpos):
        '''
        :param initpos: A position of the initial position so that we can make conditions with the currentState.
        :return: returns 0 if there is no move to be done.
        '''
        
        if self.matrix[self.currentState.row-1][self.currentState.col]=="." and self.matrix[self.currentState.row-1][self.currentState.col] != "B":
            print("NORTH")
            self.stackObject.push(0)
            self.currentState.row-=1
            self.nextState.row=self.currentState.row-1
            self.nextState.col=self.currentState.col
            self.matrix[self.currentState.row][self.currentState.col]="B"
            self.checkTreasure()
        elif self.matrix[self.currentState.row][self.currentState.col+1]=="." and self.matrix[self.currentState.row][self.currentState.col+1]!="B":
            print("EAST")
            self.stackObject.push(1)
            self.currentState.col=self.currentState.col+1
            self.nextState.row=self.currentState.row
            self.nextState.col=self.currentState.col+1
            self.matrix[self.currentState.row][self.currentState.col]="B"
            self.checkTreasure()
        elif self.matrix[self.currentState.row][self.currentState.col-1]=="." and self.matrix[self.currentState.row][self.currentState.col-1]!="B":
            print("WEST")
            self.stackObject.push(3)
            self.currentState.col=self.currentState.col-1
            self.nextState.row=self.currentState.row
            self.nextState.col=self.currentState.col-1
            self.matrix[self.currentState.row][self.currentState.col]="B"
            self.checkTreasure()
        elif self.matrix[self.currentState.row+1][self.currentState.col]=='.' and self.matrix[self.currentState.row+1][self.currentState.col]!="B":
            print("SOUTH")
            self.stackObject.push(2)
            self.nextState.row=self.currentState.row+1
            self.nextState.col=self.currentState.col
            self.currentState.row=self.currentState.row+1
            self.matrix[self.currentState.row][self.currentState.col]="B"
            self.checkTreasure()
        else:
            return 0
            
    def gamePlay(self, initpos):
        '''
        :param initpos: Takes in the initial position as a position object.
        :return: Allows flow of the function as long as we are able to move throughout the map.
        '''

        # Start moving from the initial position
        self.currentState.col = initpos.col
        self.currentState.row = initpos.row 
        
        while True:
            move = self.checkPos(initpos) # Check the position if there was a move or not. O represents no move.
            self.printMap() # Prints out the map in the form of a matrix.
            
            if move == 0: # Condition if there is no move.

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
                        self.currentState.row+=1
                    elif item == 1:
                        self.currentState.col-=1
                    elif item == 3:
                        self.currentState.col +=1
                    else:
                        self.currentState.row-=1
            else:
                continue
               
        
            
    def printMap(self):
        '''
        :return: Prints out the map of the current matrix for the user to have some feedback about the current position.
        '''
        for x in range(self.numRows):
                for y in range(self.numCols):
                    print (self.matrix[x][y])
                print("\n")
                
        
        
        