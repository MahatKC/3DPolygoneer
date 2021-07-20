from DataStructure import Object

from tkinter import *

def draw(object):
    for i in range(0, object.numberFaces):
        drawing.create_polygon(object.getCoordinates(i), outline='#f11', fill='#1f1', width=2)



window = Tk()
window.title('The Marvelous Polygoneer')
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.state('zoomed')

frameDrawingInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.7), height = int(height*(0.9)))
frameDrawingInterface.place(x = int(width*0.01), y = int(height * 0.01))

UserInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.20), height = int(height*(0.9)))
UserInterface.place(x = int(width*0.75), y = int(height * 0.01))


drawing = Canvas(frameDrawingInterface, width = int(width*0.7), height = int(height*(0.9)), bg = "white") 
drawing.pack()


obj = Object(150, 150, 150, 150, 60, 100, 17)


obj2 = Object(600, 600, 150, 150, 60, 100, 10)


obj3 = Object(400, 400, 150, 150, 60, 100, 5)

draw(obj)
draw(obj2)
draw(obj3)

window.mainloop()
