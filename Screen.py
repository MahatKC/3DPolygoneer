from DataStructure import Object
import DataStructure.Matrices.pipeline
import numpy as np
from tkinter import *

class Screen():
    def __init__(self, frame):
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

    def AddObjects(self, ):
