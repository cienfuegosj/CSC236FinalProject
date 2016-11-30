# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 09:39:56 2016
Aleksandra Cvetanovska
Javier Cienfuegos
@author: cvetanovskaa
@author: cienfuegosj
"""

from game import Game
from GUIApp import *

def main():

    fileDialog = Tk()

    '''File Dialog Properties'''

    fileDialog.wm_title("Filename Dialog")
    window_width = 300
    window_height = 100
    ws = fileDialog.winfo_screenwidth()
    hs = fileDialog.winfo_screenheight()
    x = (ws/2) - (window_width/2)
    y = (hs/2) - (window_height/2)
    fileDialog.geometry('%dx%d+%d+%d' % (window_width,window_height,x,y))
    app = FileApp(fileDialog)
    fileDialog.mainloop()
    content = app.getfileContents()


    mainDialog = Tk()

    '''Main Dialog Properties'''

    mainDialog.wm_title("Cave Backtracking")
    window_width = 700
    window_height = 500
    ws = mainDialog.winfo_screenwidth()
    hs = mainDialog.winfo_screenwidth()
    x = (ws/2) - (window_width/2)
    y = (hs/2) - (window_height/2)
    mainDialog.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    app = MainApp(mainDialog, content[0], content[1])
    mainDialog.mainloop()


main()

