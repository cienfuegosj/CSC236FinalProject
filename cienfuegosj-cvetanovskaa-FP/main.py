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


    root = Tk()
    root.wm_title("Filename Dialog")
    window_width = 300
    window_height = 100
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws/2) - (window_width/2)
    y = (hs/2) - (window_height/2)

    root.geometry('%dx%d+%d+%d' % (window_width,window_height,x,y))

    app = FileApp(root)

    root.mainloop()



    # Initialize Game
    #game = Game()
    #game.GameInit(f)


main()

