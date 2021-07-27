from DataStructure import Object
from Matrices.pipeline import pipeline_full
import numpy as np
from tkinter import *

class Screen():
    def __init__(self, frame):
        self.objects = {}
        self.number_objects = 0
        self.canvas = Canvas(frame, width = int(width*0.7), height = int(height*(0.9)), bg = "white")

    def draw(self, object):
        for i in range(0, object.numberFaces):
            x = self.canvas.create_polygon(object.getCoordinates(i), outline='blue', fill='light blue', width=2, tags = "objeto")
            

window = Tk()
window.title('The Marvelous Polygoneer')
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.state('zoomed')

frameDrawingInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.7), height = int(height*(0.9)))
frameDrawingInterface.place(x = int(width*0.01), y = int(height * 0.01))

UserInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.20), height = int(height*(0.9)))
UserInterface.place(x = int(width*0.75), y = int(height * 0.01))


#drawing = Canvas(frameDrawingInterface, width = int(width*0.7), height = int(height*(0.9)), bg = "white") 
drawing = Screen()
drawing.pack()



poliedro_teste = np.array([[30, 35, 25, 20,   30],
                           [ 2,  4,  3,  1,   10],
                           [25, 20, 18, 23, 22.5],
                           [ 1,  1,  1,  1,    1]])


obj4 = pipeline_full(poliedro_teste, 50, 15, 30, 20, 6, 15, 0, 1, 0, 10, 40, True, 17, -8, 8, -5, 5, 320, 0, 240, 0)



def which_object(x, y):
    x = 10

def object_clicked(event):
    print("voce cricou no objeto")
    drawing.delete("current")
    which_object(event.x, event.y)

drawing.tag_bind("objeto", "<Button-1>", object_clicked)

def draw_objects(event):
    obj = Object(450, 150, 150, 150, 60, 100, 20)
    obj2 = Object(600, 600, 150, 150, 60, 100, 10)
    obj3 = Object(400, 400, 150, 150, 60, 100, 5)
    obj4 = Object(150, 150, 150, 150, 60, 100, 17)
    obj5 = Object(650, 150, 250, 250, 60, 100, 3)
    obj6 = Object(1000, 400, 250, 250, 60, 100, 18)

    draw(obj)
    draw(obj2)
    draw(obj3)
    draw(obj4)
    draw(obj5)
    draw(obj6)


def erase(event):
    if event.char == ' ':
        print("test")
        drawing.delete(ALL)

drawing.bind_all('<space>', erase)
drawing.bind_all('<x>', draw_objects)

window.mainloop()
