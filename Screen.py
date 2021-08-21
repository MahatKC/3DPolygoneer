#from exemplo_prova import exemplo_prova
from DataStructure.DataStructure import Object
from DataStructure.Axis import Axis
from DataStructure.Matrices.pipeline import first_pipeline, VRP_and_n, pipeline_steps
import numpy as np 
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)
from tkinter import *
import random
# apagar também das listas quando trabalhar com os objetos
class Screen():
    def __init__(self, frame, width, height):
        self.polygonsColors = ['#F54C99', '#FF4FF8', '#C354E8', '#A34FFF', '#6E4CF5']
        self.isPerspective = False

        self.maxXviewPort = int(width)
        self.maxYviewPort = int(height*(0.88))

        self.mundoXmin = -50
        self.mundoXmax = 40
        self.mundoYmin = -40
        self.mundoYmax = 30
        
        self.projecaoXmin = 0
        self.projecaoXmax = self.maxXviewPort
        self.projecaoYmin = 0
        self.projecaoYmax = self.maxYviewPort

        self.VRPx = 100
        self.VRPy = -50
        self.VRPz = 70

        self.Px = 2
        self.Py = 1
        self.Pz = 3

        self.ViewUpX = 0
        self.ViewUpY = 1
        self.ViewUpZ = 0
        
        self.nearValue = 10
        self.farValue = 1000
        self.distanciaProjecao = 50

        self.VRP, self.n = VRP_and_n(self.VRPx, self.VRPy, self.VRPz, self.Px, self.Py, self.Pz)  
        self.SRC, self.jp_times_proj = first_pipeline(self.VRP, self.n, self.ViewUpX, self.ViewUpY, self.ViewUpZ, self.isPerspective, self.distanciaProjecao, self.mundoXmin, self.mundoXmax, self.mundoYmin, self.mundoYmax, self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
        self.objects = []
        self.objectsInCanvas = [] # list of all the objects with all the faces that each one has
        self.numberObjects = 0
        self.canvas = Canvas(frame, width = self.maxXviewPort, height = self.maxYviewPort, bg = "white")
        self.objectSelected = None 
        self.viewPort = self.canvas.create_polygon([self.projecaoXmin,self.projecaoYmin, self.projecaoXmin, self.projecaoYmax, self.projecaoXmax, self.projecaoYmax, self.projecaoXmax, self.projecaoYmin], outline= "#CCCCCC", fill= "#CCCCCC", width = 3)
     
        self.DefineAxis()

    def DefineAxis(self):
        axis = Axis()
        
        axis.pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
        #axis.translation(-25, -25, 0)
        #axis.pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
        #x = int(axis.axisSRT[0][0] - int(self.maxXviewPort * 0.07))
        #y = int(axis.axisSRT[1][0] - int(self.maxYviewPort * 0.93))
        self.canvas.create_line(axis.axisSRT[0][0], axis.axisSRT[1][0], axis.axisSRT[0][1], axis.axisSRT[1][1], fill='#FF0000', width = 5)
        self.canvas.create_line(axis.axisSRT[0][0], axis.axisSRT[1][0], axis.axisSRT[0][2], axis.axisSRT[1][2], fill='#00FF00', width = 5)
        self.canvas.create_line(axis.axisSRT[0][0], axis.axisSRT[1][0], axis.axisSRT[0][3], axis.axisSRT[1][3], fill='#0000FF', width = 5)
        
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
        list.append(self.nearValue)
        list.append(self.farValue)
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
        
        self.isPerspective = isPerspective

        if projecaoXmin < 0:
            projecaoXmin = 0
        if projecaoXmax > self.maxXviewPort:
            projecaoXmax = self.maxXviewPort
        if projecaoYmin < 0:
            projecaoYmin = 0
        if projecaoYmax > self.maxYviewPort:
            projecaoYmax = self.maxYviewPort

        self.mundoXmin = mundoXmin
        self.mundoXmax = mundoXmax
        self.mundoYmin = mundoYmin
        self.mundoYmax = mundoYmax
        
        self.projecaoXmin = projecaoXmin
        self.projecaoXmax = projecaoXmax
        self.projecaoYmin = projecaoYmin
        self.projecaoYmax = projecaoYmax

        self.VRPx = VRPx
        self.VRPy = VRPy
        self.VRPz = VRPz

        self.Px = Px
        self.Py = Py
        self.Pz = Pz

        self.ViewUpX = ViewUpX
        self.ViewUpY = ViewUpY
        self.ViewUpZ = ViewUpZ
        
        self.nearValue = near
        self.farValue = far
        self.distanciaProjecao = distanciaProjecao
        self.objectSelected = None
        
        self.VRP, self.n = VRP_and_n(VRPx, VRPy, VRPz, Px, Py, Pz)  
        self.SRC, self.jp_times_proj = first_pipeline(self.VRP, self.n, ViewUpX, ViewUpY, ViewUpZ, isPerspective, distanciaProjecao, mundoXmin, mundoXmax, mundoYmin, mundoYmax, projecaoXmin, projecaoXmax, projecaoYmin, projecaoYmax)
        
        for object in range(self.numberObjects):
            self.objects[object].normalVisualizationTest(self.n)
            self.objects[object].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[object].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
        
        self.Draw()

    def ClearAll(self):
        self.canvas.delete(ALL)
        self.objects.clear()
        self.objectsInCanvas.clear()
        self.viewPort = self.canvas.create_polygon([self.projecaoXmin,self.projecaoYmin, self.projecaoXmin, self.projecaoYmax, self.projecaoXmax, self.projecaoYmax, self.projecaoXmax, self.projecaoYmin], outline= "#CCCCCC", fill="#CCCCCC", width = 2)
        self.numberObjects = 0
        
        self.DefineAxis()

    def Draw(self):
        self.canvas.delete(ALL)
        self.objectsInCanvas.clear()
        self.viewPort = self.canvas.create_polygon([self.projecaoXmin,self.projecaoYmin, self.projecaoXmin, self.projecaoYmax, self.projecaoXmax, self.projecaoYmax, self.projecaoXmax, self.projecaoYmin], outline="#CCCCCC", fill="#CCCCCC", width = 2)
        for objects in range(self.numberObjects): # gerar uma lista com a ordem de todos os objetos em Z
            self.objectsInCanvas.append([])
            for viewport_face_idx in range(len(self.objects[objects].viewport_faces)):
                self.objectsInCanvas[objects].append(self.canvas.create_polygon(self.objects[objects].getCoordinates(viewport_face_idx), outline= random.choice(self.polygonsColors), fill=random.choice(self.polygonsColors), width = 2, tags = "objeto"))
        
        self.DefineAxis()

    def moveObject(self, valueX, valueY, valueZ):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].translation(valueX, valueY, valueZ)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.Draw()
    
    def scaleObject(self, Sx, Sy, Sz):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].scale(Sx, Sy, Sz)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.Draw()

    def rotObjectX(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationX(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.Draw()

    def rotObjectY(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationY(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.Draw()

    def rotObjectZ(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationZ(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.Draw()

    def AddObjects(self, r_bottom, r_top, sides, h):
        new_obj = Object(0, 0, 0, h, r_bottom, r_top, sides) 
        new_obj.normalVisualizationTest(self.n)
        new_obj.pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
        new_obj.crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
        self.objects.append(new_obj) 
        self.objectsInCanvas.append([])
        
        for viewport_face_idx in range(len(new_obj.viewport_faces)):
            self.objectsInCanvas[self.numberObjects].append(self.canvas.create_polygon(new_obj.getCoordinates(viewport_face_idx), outline= random.choice(self.polygonsColors), fill= random.choice(self.polygonsColors), width = 2, tags = "objeto"))
 
        self.numberObjects += 1
    
    def UpdateObject(self, r_bottom, r_top, sides, h):
        new_obj = Object(0, 0, 0, h, r_bottom, r_top, sides) # alterar o X, Y e Z para pegar o do objeto atual
        new_obj.normalVisualizationTest(self.n)
        new_obj.pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
        new_obj.crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
        self.objects[self.objectSelected] = new_obj 
        self.Draw()