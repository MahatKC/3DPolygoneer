#from exemplo_prova import exemplo_prova
from DataStructure.DataStructure import Object
from DataStructure.Matrices.pipeline import first_pipeline, VRP_and_n, pipeline_steps
import numpy as np 
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)
from tkinter import *
# apagar também das listas quando trabalhar com os objetos
class Screen():
    def __init__(self, frame, width, height):
        self.isPerspective = False

        self.mundoXmin = -50
        self.mundoXmax = 40
        self.mundoYmin = -40
        self.mundoYmax = 30
        
        self.projecaoXmin = 300
        self.projecaoXmax = 1000
        self.projecaoYmin = 200
        self.projecaoYmax = 600

        self.VRPx = 100
        self.VRPy = -50
        self.VRPz = 70

        self.Px = 2
        self.Py = 1
        self.Pz = 3

        self.ViewUpX = 0
        self.ViewUpY = 1
        self.ViewUpZ = 0
        
        self.near_value = 10
        self.far_value = 1000
        self.distanciaProjecao = 50

        self.VRP, self.n = VRP_and_n(self.VRPx, self.VRPy, self.VRPz, self.Px, self.Py, self.Pz)  
        self.SRC, self.jp_times_proj = first_pipeline(self.VRP, self.n, self.ViewUpX, self.ViewUpY, self.ViewUpZ, self.isPerspective, self.distanciaProjecao, self.mundoXmin, self.mundoXmax, self.mundoYmin, self.mundoYmax, self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
        self.objects = []
        self.objectsInCanvas = [] # list of all the objects with all the faces that each one has
        self.numberObjects = 0
        self.canvas = Canvas(frame, width = int(width*0.7), height = int(height*(0.88)), bg = "white")
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
                self.objectSelected = i
                return self.objects[i] 

    def ObjectSelection(self, face):
        for object in range(self.numberObjects):
            if face in self.objectsInCanvas[object]:
                self.objectSelected = object
                return self.objectsInCanvas[object]
    
    def GetAttributes(self):
        list = []
        list.append(self.objects[self.objectSelected].sides)
        list.append(self.objects[self.objectSelected].r_bottom)
        list.append(self.objects[self.objectSelected].r_top)
        list.append(self.objects[self.objectSelected].height)
        return list
        
    def GetProjecao(self):
        list = []
        list.append(self.VRPx)
        list.append(self.VRPy)
        list.append(self.VRPz)
        list.append(self.Px)
        list.append(self.Py)
        list.append(self.Pz)
        list.append(self.ViewUpX)
        list.append(self.ViewUpY)
        list.append(self.ViewUpZ)
        list.append(self.near_value)
        list.append(self.far_value)
        list.append(self.distanciaProjecao)
        list.append(self.mundoXmin)
        list.append(self.mundoXmax)
        list.append(self.mundoYmin)
        list.append(self.mundoYmax)
        list.append(self.projecaoXmin)
        list.append(self.projecaoXmax)
        list.append(self.projecaoYmin)
        list.append(self.projecaoYmax)
        return list

    def RedoPipeline(self, isPerspective, VRPx, VRPy, VRPz, Px, Py, Pz, ViewUpX, ViewUpY, ViewUpZ, near, far, distanciaProjecao,
                mundoXmin, mundoXmax, mundoYmin, mundoYmax, projecaoXmin, projecaoXmax, projecaoYmin, projecaoYmax):
        self.VRP, self.n = VRP_and_n(VRPx, VRPy, VRPz, Px, Py, Pz)  
        self.near_value = near
        self.far_value = far
        self.SRC, self.jp_times_proj = first_pipeline(self.VRP, self.n, ViewUpX, ViewUpY, ViewUpZ, isPerspective, distanciaProjecao, mundoXmin, mundoXmax, mundoYmin, mundoYmax, projecaoXmin, projecaoXmax, projecaoYmin, projecaoYmax)
        
        for object in range(self.numberObjects):
            self.objects[object].normalVisualizationTest(self.n)
            self.objects[object].pipeline_me(self.SRC, self.jp_times_proj, self.near_value, self.far_value)
        
        self.Draw()

    def ClearAll(self):
        self.canvas.delete(ALL)
        self.objects.clear()
        self.objectsInCanvas.clear()
        self.numberObjects = 0

    def Draw(self):
        self.canvas.delete(ALL)
        self.objectsInCanvas.clear()
        for objects in range(self.numberObjects): # gerar uma lista com a ordem de todos os objetos em Z
            self.objectsInCanvas.append([])
            for faces in range(self.objects[objects].numberFaces): # gerar uma lista com as faces do objeto em Z
                if(self.objects[objects].draw_faces[faces]):
                    self.objectsInCanvas[objects].append(self.canvas.create_polygon(self.objects[objects].getCoordinates(faces), outline='blue', fill='light blue', width = 2, tags = "objeto"))
                

    def moveObject(self, valueX, valueY, valueZ):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].translation(valueX, valueY, valueZ)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.near_value, self.far_value)
            self.Draw()
    
    def scaleObject(self, Sx, Sy, Sz):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].scale(Sx, Sy, Sz)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.near_value, self.far_value)
            self.Draw()

    def rotObjectX(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationX(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.near_value, self.far_value)
            self.Draw()

    def rotObjectY(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationY(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.near_value, self.far_value)
            self.Draw()

    def rotObjectZ(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationZ(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.near_value, self.far_value)
            self.Draw()

    def AddObjects(self, r_bottom, r_top, sides, h):
        new_obj = Object(0, 0, 0, h, r_bottom, r_top, sides) 
        new_obj.normalVisualizationTest(self.n)
        new_obj.pipeline_me(self.SRC, self.jp_times_proj, self.near_value, self.far_value)
        self.objects.append(new_obj) 
        self.objectsInCanvas.append([])
        
        for i in range(new_obj.numberFaces):
            if(new_obj.draw_faces[i]):
                self.objectsInCanvas[self.numberObjects].append(self.canvas.create_polygon(new_obj.getCoordinates(i), outline='blue', fill='light blue', width = 2, tags = "objeto"))
        
        self.numberObjects += 1
    
    def UpdateObject(self, r_bottom, r_top, sides, h):
        new_obj = Object(0, 0, 0, h, r_bottom, r_top, sides) # alterar o X, Y e Z para pegar o do objeto atual
        new_obj.normalVisualizationTest(self.n)
        new_obj.pipeline_me(self.SRC, self.jp_times_proj, self.near_value, self.far_value)
        self.objects[self.objectSelected] = new_obj 
        self.Draw()

    """def AddObjectsProva(self, r_bottom, r_top, sides, h):
        new_obj = exemplo_prova() 
        new_obj.normalVisualizationTest(self.n)
        new_obj.pipeline_me(self.SRC, self.jp_times_proj, 10, 1000)
        self.objects.append(new_obj) 
        self.objectsInCanvas.append([])
        
        print(new_obj.draw_faces)
        print(new_obj.prism_in_SRT)
        for i in range(new_obj.numberFaces):
            if(new_obj.draw_faces[i]):
                self.objectsInCanvas[self.numberObjects].append(self.canvas.create_polygon(new_obj.getCoordinates(i), outline='blue', fill='light blue', width = 2, tags = "objeto"))

        # 
        self.numberObjects += 1"""
"""

window = Tk()
window.title('The Marvelous Polygoneer')
width = window.winfo_screenwidth() 
height = window.winfo_screenheight()
window.state('zoomed')

frameDrawingInterface = Frame(window, highlightbackground= "black", highlightthickness= 1, width = int(width*0.7), height = int(height*(0.9)))
frameDrawingInterface.place(x = int(width*0.01), y = int(height * 0.01))

UserInterface = Frame(window, highlightbackground= "black", highlightthickness= 1, width = int(width*0.20), height = int(height*(0.9)))
UserInterface.place(x = int(width*0.75), y = int(height * 0.01))


drawing = Screen(frameDrawingInterface, width, height)

drawing.canvas.pack()

def draw_objects1(event):
    drawing.AddObjects(40, 20, 8, 50) 

def draw_objects2(event):
    drawing.AddObjects(150, 60, 20, 10)

def draw_objects3(event):
    drawing.AddObjects(150, 60, 4, 5)

def draw_objects4(event):
    drawing.AddObjects(150, 100, 12, 20) 
    
def draw_objects5(event):
    drawing.AddObjects(150, 100, 12, 10) 

def draw_objects6(event):
    drawing.AddObjects(150, 100, 12, 5)   

drawing.canvas.bind_all('<q>', draw_objects1) 
drawing.canvas.bind_all('<w>', draw_objects2) 
drawing.canvas.bind_all('<e>', draw_objects3) 
drawing.canvas.bind_all('<r>', draw_objects4) 
drawing.canvas.bind_all('<t>', draw_objects5) 
drawing.canvas.bind_all('<y>', draw_objects6) 

def draw_objects2(event):
    drawing.AddObjectsProva(30, 60, 15, 90) 
drawing.canvas.bind_all('<c>', draw_objects2)

def erase(event):
    drawing.canvas.delete("current")

def selectObject(event):
    if event.widget.find_withtag("current"):
        object = drawing.ObjectSelection(drawing.canvas.find_withtag("current")[0])
        for i in object:
            drawing.canvas.itemconfig(i, fill='red')
            drawing.canvas.coords(i, [30, 30, 50, 80, 100, 100, 200, 200, 420, 100]) #readapta as coordenadas de cada face do objeto
    else:
        drawing.objectSelected = None
    
drawing.canvas.bind('<Button-1>', erase)
#drawing.canvas.bind('<Button-1>', selectObject)"""
