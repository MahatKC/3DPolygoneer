from DataStructure import Object
from DataStructure.Matrices.pipeline import first_pipeline, VRP_and_n, pipeline_steps
import numpy as np
from tkinter import *

class Screen():
    def __init__(self, frame, width, height):
        self.VRP, self.n = VRP_and_n(200, 200, 200, 0, 0, 0) 
        self.SRC, self.jp_times_proj = first_pipeline(self.VRP, self.n, 0, 1, 0, True, 150, -200, 200, -200, 200, width, 0, height, 0)
        self.objects = []
        self.number_objects = 0
        self.canvas = Canvas(frame, width = int(width*0.7), height = int(height*(0.9)), bg = "white")
        self.object_Selected = None

    def draw(self, object):
        self.objects[self.number_objects] = []
        for i in range(0, object.numberFaces):
            self.objects[self.number_objects].append(self.canvas.create_polygon(object.getCoordinates(i), outline='blue', fill='light blue', width = 2, tags = "objeto"))
        self.number_objects = self.number_objects + 1

    def deleteObject(self, face):
        for i in range(0, self.number_objects):
            if face in self.objects[i]:
                self.object_Selected = i
                return self.objects[i]

    def AddObjects(self, r_bottom, r_top, sides, h):
        new_obj = Object(0, 0, 0, h, r_bottom, r_top, sides)
        new_obj.normalVisualizationTest(self.n)
        self.objects.append(new_obj)

        

