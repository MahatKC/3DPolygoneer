from DataStructure.DataStructure import Object
from DataStructure.Axis import Axis
from DataStructure.Matrices.pipeline import first_pipeline, VRP_and_n
import numpy as np 
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)
from tkinter import *
class Screen():
    def __init__(self, frame, width, height):
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

        if self.isPerspective:
            self.Px = 2
            self.Py = 1
            self.Pz = 3
        else:
            self.Px = 0
            self.Py = 0
            self.Pz = 0

        self.ViewUpX = 0
        self.ViewUpY = 1
        self.ViewUpZ = 0

        self.il = [255, 255, 255]
        self.ila = [255, 255, 255]
        self.fonteLuz = [0, 1000, 0]
        
        self.nearValue = 10
        self.farValue = 1000
        self.distanciaProjecao = 50

        self.objects_Z_order = []

        self.VRP, self.n = VRP_and_n(self.VRPx, self.VRPy, self.VRPz, self.Px, self.Py, self.Pz)  
        self.SRC, self.jp_times_proj = first_pipeline(self.VRP, self.n, self.ViewUpX, self.ViewUpY, self.ViewUpZ, self.isPerspective, self.distanciaProjecao, self.mundoXmin, self.mundoXmax, self.mundoYmin, self.mundoYmax, self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
        self.objects = []
        self.objectsInCanvas = [] # list of all the objects with all the faces that each one has
        self.numberObjects = 0
        self.canvas = Canvas(frame, width = self.maxXviewPort, height = self.maxYviewPort, bg = "white")
        self.objectSelected = None 
        self.viewPort = self.canvas.create_polygon([self.projecaoXmin - 1,self.projecaoYmin - 1, self.projecaoXmin - 1, self.projecaoYmax + 1, self.projecaoXmax + 1, self.projecaoYmax + 1, self.projecaoXmax + 1, self.projecaoYmin - 1], outline= "#000000", fill= "#CCCCCC", width = 2)

        self.endLineX = [2]
        self.endLineY = [2]
        self.endLineZ = [2]
        self.DefineAxis()

    def DefineAxis(self):
        axis = Axis()
        axisSRC, _ = first_pipeline(self.VRP, self.n, self.ViewUpX, self.ViewUpY, self.ViewUpZ, self.isPerspective, self.distanciaProjecao, self.mundoXmin, self.mundoXmax, self.mundoYmin, self.mundoYmax, 0, self.maxXviewPort, 0, self.maxYviewPort)
        
        axis.pipeline_me(axisSRC, self.isPerspective, self.distanciaProjecao)

        x = int(axis.axisSRT[0][0] - 70)
        y = int(axis.axisSRT[1][0] - 569)

        self.endLineX = [axis.axisSRT[0][1] - x, axis.axisSRT[1][1] - y]
        self.endLineY = [axis.axisSRT[0][2] - x, axis.axisSRT[1][2] - y]
        self.endLineZ = [axis.axisSRT[0][3] - x, axis.axisSRT[1][3] - y]
        self.canvas.create_line(axis.axisSRT[0][0] - x, axis.axisSRT[1][0] - y, self.endLineX[0], self.endLineX[1], fill='#FFF000000', width = 5)
        self.canvas.create_line(axis.axisSRT[0][0] - x, axis.axisSRT[1][0] - y, self.endLineY[0], self.endLineY[1], fill='#000FFF000', width = 5)
        self.canvas.create_line(axis.axisSRT[0][0] - x, axis.axisSRT[1][0] - y, self.endLineZ[0], self.endLineZ[1], fill='#000000FFF', width = 5)

    def PosEixos(self):
        return [self.endLineX, self.endLineY, self.endLineZ]

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
        list.append(self.objects[self.objectSelected].n)
        list.append(self.objects[self.objectSelected].ka[0])
        list.append(self.objects[self.objectSelected].ka[1])
        list.append(self.objects[self.objectSelected].ka[2])
        list.append(self.objects[self.objectSelected].kd[0])
        list.append(self.objects[self.objectSelected].kd[1])
        list.append(self.objects[self.objectSelected].kd[2])
        list.append(self.objects[self.objectSelected].ks[0])
        list.append(self.objects[self.objectSelected].ks[1])
        list.append(self.objects[self.objectSelected].ks[2])
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
        list.append(self.il)
        list.append(self.ila)
        list.append(self.fonteLuz)
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

        if isPerspective:
            self.Px = Px
            self.Py = Py
            self.Pz = Pz
        else:
            self.Px = 0
            self.Py = 0
            self.Pz = 0

        self.ViewUpX = ViewUpX
        self.ViewUpY = ViewUpY
        self.ViewUpZ = ViewUpZ
        
        self.nearValue = near
        self.farValue = far
        self.distanciaProjecao = distanciaProjecao
        self.objectSelected = None
        
        self.VRP, self.n = VRP_and_n(self.VRPx, self.VRPy, self.VRPz, self.Px, self.Py, self.Pz)  
        self.SRC, self.jp_times_proj = first_pipeline(self.VRP, self.n, ViewUpX, ViewUpY, ViewUpZ, isPerspective, distanciaProjecao, mundoXmin, mundoXmax, mundoYmin, mundoYmax, projecaoXmin, projecaoXmax, projecaoYmin, projecaoYmax)
        
        for object in range(self.numberObjects):
            self.objects[object].normalVisualizationTest(self.n)
            self.objects[object].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[object].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.objects[object].FacesOrder()
            self.objects[object].sombreamento_constante(self.VRP, self.il, self.ila, self.fonteLuz)
        
        self.Draw()

    def ChangeIlumination(self, sombreamento, ila, il, fonteLuz):
        self.il = il
        self.ila = ila
        self.fonteLuz = fonteLuz
        self.Draw()

    def ClearAll(self):
        self.canvas.delete(ALL)
        self.objects.clear()
        self.objectsInCanvas.clear()
        self.viewPort = self.canvas.create_polygon([self.projecaoXmin - 1,self.projecaoYmin - 1, self.projecaoXmin - 1, self.projecaoYmax + 1, self.projecaoXmax + 1, self.projecaoYmax + 1, self.projecaoXmax + 1, self.projecaoYmin - 1], outline= "#000000", fill= "#CCCCCC", width = 2)
        self.numberObjects = 0
        
        self.DefineAxis()

    def Draw(self):
        self.canvas.delete(ALL)
        self.objectsInCanvas = [None] * self.numberObjects 
        self.viewPort = self.canvas.create_polygon([self.projecaoXmin - 1,self.projecaoYmin - 1, self.projecaoXmin - 1, self.projecaoYmax + 1, self.projecaoXmax + 1, self.projecaoYmax + 1, self.projecaoXmax + 1, self.projecaoYmin - 1], outline= "#000000", fill= "#CCCCCC", width = 2)
        self.PolygonsOrder()
        for objects in self.objects_Z_order: # percorrer uma lista com a ordem de todos os objetos em Z
            if self.objects[objects].draw_me:
                self.objects[objects].sombreamento_constante(self.VRP, self.il, self.ila, self.fonteLuz)
                self.objectsInCanvas[objects] = []
                if(objects == self.objectSelected):
                    for viewport_face_idx in self.objects[objects].faces_order:
                        self.objectsInCanvas[objects].append(self.canvas.create_polygon(self.objects[objects].getCoordinates(viewport_face_idx), outline= "#000000", fill= self.objects[objects].color_of_faces[viewport_face_idx], width = 2, tags = "objeto"))
                else:
                    for viewport_face_idx in self.objects[objects].faces_order:
                        self.objectsInCanvas[objects].append(self.canvas.create_polygon(self.objects[objects].getCoordinates(viewport_face_idx), outline= self.objects[objects].color_of_faces[viewport_face_idx], fill= self.objects[objects].color_of_faces[viewport_face_idx], width = 2, tags = "objeto"))

        self.DefineAxis()

    def moveObject(self, valueX, valueY, valueZ):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].translation(valueX, valueY, valueZ)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.objects[self.objectSelected].FacesOrder()
            self.Draw()
    
    def scaleObject(self, Sx, Sy, Sz):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].scale(Sx, Sy, Sz)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.objects[self.objectSelected].FacesOrder()
            self.Draw()

    def rotObjectX(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationX(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.objects[self.objectSelected].FacesOrder()
            self.Draw()

    def rotObjectY(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationY(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.objects[self.objectSelected].FacesOrder()
            self.Draw()

    def rotObjectZ(self, rotationValue):
        if(self.objectSelected is not None):
            self.objects[self.objectSelected].rotationZ(rotationValue)
            self.objects[self.objectSelected].normalVisualizationTest(self.n)
            self.objects[self.objectSelected].pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
            self.objects[self.objectSelected].crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
            self.objects[self.objectSelected].FacesOrder()
            self.Draw()

    def AddObjects(self, r_bottom, r_top, sides, h, ka, kd, ks, n):
        new_obj = Object(0, 0, 0, h, r_bottom, r_top, sides, ka, kd, ks, n) 
        new_obj.normalVisualizationTest(self.n)
        new_obj.pipeline_me(self.SRC, self.jp_times_proj, self.nearValue, self.farValue)
        new_obj.crop_to_screen(self.projecaoXmin, self.projecaoXmax, self.projecaoYmin, self.projecaoYmax)
        new_obj.FacesOrder()
        new_obj.sombreamento_constante(self.VRP, self.il, self.ila, self.fonteLuz)
        self.objects.append(new_obj) 
        self.objectsInCanvas.append([])
        self.numberObjects += 1
        self.Draw()
    
    def UpdateObject(self, ka, kd, ks, n):
        self.objects[self.objectSelected].ka = ka 
        self.objects[self.objectSelected].kd = kd 
        self.objects[self.objectSelected].ks = ks 
        self.objects[self.objectSelected].n = n
        self.objects[self.objectSelected].sombreamento_constante(self.VRP, self.il, self.ila, self.fonteLuz)
        self.Draw()

    def PolygonsOrder(self):
        self.objects_Z_order.clear()
        objects_z_list = [self.objects[i].object_min_z for i in range(self.numberObjects)]
        self.objects_Z_order = np.argsort(objects_z_list).tolist()