"""
Created on Mon Oct 24 09:39:56 2016
Aleksandra Cvetanovska
Javier Cienfuegos
@author: cvetanovskaa
@author: cienfuegosj
"""


from GUIApp import *
import turtle

def main():

    fileDialog = Tk() # Tk object to pass into application

    '''File Dialog Properties'''

    fileDialog.wm_title("Filename Dialog")
    window_width = 300
    window_height = 100
    ws = fileDialog.winfo_screenwidth()
    hs = fileDialog.winfo_screenheight()
    x = (ws/2) - (window_width/2)
    y = (hs/2) - (window_height/2)
    fileDialog.geometry('%dx%d+%d+%d' % (window_width,window_height,x,y))

    ''' The properties above are to center the file dialog when the user first invokes the application.'''


    app = FileApp(fileDialog) # FileApp object to handle Tk object methods and functionality
    fileDialog.mainloop() # Allows us to loop until the user exits the dialog
    content = app.getfileContents() # receives the content from the application

    EditorDialog = Tk()  # Tk object to pass into application

    '''Editor Dialog Properties'''

    EditorDialog.wm_title("Editor Dialog")
    window_width = 500
    window_height = 1000
    ws = EditorDialog.winfo_width()
    hs = EditorDialog.winfo_height()
    x = (ws / 2) - (window_width / 2)
    y = (hs / 2) - (window_height / 2)
    EditorDialog.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    ''' The properties above are to allow start the application in the correct position'''

    edit = EditorApp(EditorDialog)
    EditorDialog.mainloop()
    colors = edit.getcolors()

    main = MainApp(content[0], content[1], colors) # Turtle window application where content[0] is the matrix and content[1] is initial position

main()

