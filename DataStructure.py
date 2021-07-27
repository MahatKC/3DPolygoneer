from Matrices.prism import create_prism
import numpy as np
import math

#counter clockwise
#fazer as funções para chamar os métodos do objeto
class Object():
    def __init__(self, x, y, z, h, r_bottom, r_top, sides):
        self.vertex = create_prism(x, y, z, h, r_bottom, r_top, sides)
        self.faces = {}
        self.vertexFaces = {} 
        self.numberFaces = sides + 2
        self.sides = sides

        for i in range(0, sides):
            self.faces[i] =  (i, (i + 1) % sides, ((i + 1) % sides) + sides , i + sides)
        self.faces[sides] = (np.arange(sides))
        self.faces[sides + 1] = (np.arange(sides) + sides)
        
        for i in range (0, sides * 2):
            self.vertexFaces[i] = (i % sides, (i + sides - 1) % sides, math.floor(i / sides) + sides)

    def getCoordinates(self, face):
        list = []
        for i in range(0, len(self.faces[face])):
            list.append(int(self.vertex[0][self.faces[face][i]]))
            list.append(int(self.vertex[1][self.faces[face][i]]))     
        return list

obj = Object(150, 150, 150, 150, 60, 100, 6)