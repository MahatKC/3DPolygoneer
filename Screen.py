from DataStructure.DataStructure import Object
from DataStructure.Matrices.pipeline import first_pipeline, VRP_and_n, pipeline_steps
import numpy as np
from tkinter import *

class Screen():
    def __init__(self, frame, width, height):
        self.VRP, self.n = VRP_and_n(200, 200, 0, width, height, 0)  
        self.SRC, self.jp_times_proj = first_pipeline(self.VRP, self.n, 0, 1, 0, True, 150, -200, 200, -200, 200, width, 0, height, 0)
        self.objects = [] 
        self.objectsInCanvas = [] # list of all the objects with all the faces that each one has
        self.numberObjects = 0
        self.canvas = Canvas(frame, width = int(width*0.7), height = int(height*(0.9)), bg = "white")
        self.objectSelected = None

    #def draw(self, object):
    #    self.objects[self.number_objects] = []
    #    for i in range(0, object.numberFaces): 
    #        self.objects[self.number_objects].append(self.canvas.create_polygon(object.getCoordinates(i), outline='blue', fill='light blue', width = 2, tags = "objeto"))
    #    self.number_objects = self.number_objects + 1
    #def draw(object):


    def deleteObject(self, face):
        for i in range(0, self.numberObjects):
            if face in self.objects[i]:
                self.object_Selected = i
                return self.objects[i] 

    def ObjectSelection(self, face):
        for object in range(self.numberObjects):
            if face in self.objectsInCanvas[object]:
                self.objectSelected = object
                return self.objectsInCanvas[object]


    def AddObjects(self, r_bottom, r_top, sides, h):
        new_obj = Object(width//3, height//3, 0, h, r_bottom, r_top, sides)
        new_obj.normalVisualizationTest(self.n)
        new_obj.pipeline_me(self.SRC, self.jp_times_proj, 10, 1000)
        self.objects.append(new_obj) 
        self.objectsInCanvas.append([])
        
        for i in range(new_obj.numberFaces):
            j=0
            if(new_obj.draw_faces[i]):
                self.objectsInCanvas[self.numberObjects].append(self.canvas.create_polygon(new_obj.getCoordinates(i,j), outline='blue', fill='light blue', width = 2, tags = "objeto"))
                j+=1
        
        self.numberObjects += 1


window = Tk()
window.title('The Marvelous Polygoneer')
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.state('zoomed')

frameDrawingInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.7), height = int(height*(0.9)))
frameDrawingInterface.place(x = int(width*0.01), y = int(height * 0.01))

UserInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.20), height = int(height*(0.9)))
UserInterface.place(x = int(width*0.75), y = int(height * 0.01))


drawing = Screen(frameDrawingInterface, width, height)

drawing.canvas.pack()

def draw_objects(event):
    drawing.AddObjects(40, 20, 8, 50) 
drawing.canvas.bind_all('<x>', draw_objects)

def draw_objects2(event):
    drawing.AddObjects(30, 60, 15, 90) 
drawing.canvas.bind_all('<c>', draw_objects2)

def erase(event):
    drawing.canvas.delete("current")

def selectObject(event):
    if event.widget.find_withtag("current"):
        object = drawing.ObjectSelection(drawing.canvas.find_withtag("current")[0])
        for i in object:
            drawing.canvas.itemconfig(i, fill='red')
    else:
        drawing.objectSelected = None
    
#drawing.canvas.bind('<Button-1>', erase)
drawing.canvas.bind('<Button-1>', selectObject)
            

window.mainloop()

#calculo da normal só diz se aquela face é possível de ser vista pelo observador, não diz se uma outra face tamparia