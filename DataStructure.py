from Matrices.prism import create_prism
from Matrices.normal_test import normal_test
import numpy as np
import math

#counter clockwise
#fazer as funções para chamar os métodos do objeto
#quando clicar em um objeto, selecionar o objeto que esta sendo clicado
#fazer uma lista de objetos que estão existindo
#fazer um modo de ao clicar selecionar um dos objetos do tkinter
#fazer um modo de alterar esse objeto do tkinter e alterar na lista
#ver se consegue ao clicar pegar por exemplo a cor que esta o pixel na coordenada clicada, além de pegar a posição X e Y
#Desselecionar o objeto ao apertar no branco da tela
#enviar o objeto pra fazer TG
class Object():
    def __init__(self, x, y, z, h, r_bottom, r_top, sides):
        self.vertex = create_prism(x, y, z, h, r_bottom, r_top, sides)
        self.faces = []
        self.draw_faces = []
        self.vertexFaces = []
        self.draw_vertex = [False]*sides*2
        self.numberFaces = sides + 2
        self.sides = sides

        sides_minus_one = sides*2-1
        for f in range(0, sides):
            complement_of_next = (f+1)%sides
            self.faces.append([f, sides_minus_one-f, sides_minus_one-complement_of_next, complement_of_next])
        self.faces.append(np.arange(sides).tolist())
        self.faces.append((np.arange(sides) + sides).tolist())
        
        for v in range(0, sides*2):
            floor = np.floor(v/sides)
            self.vertexFaces.append([v%sides, (sides*(1+floor))-v-1, floor+sides])

    def getCoordinates(self, face):
        list = []
        for i in range(0, len(self.faces[face])):
            list.append(int(self.vertex[0][self.faces[face][i]]))
            list.append(int(self.vertex[1][self.faces[face][i]]))     
        return list

    def normalVisualizationTest(self, n):
        for face in self.faces:
            face_vertices = []
            for i in range(3):
                face_vertices.append(self.vertex[face[i]])
            draw_this_face = normal_test(face_vertices)
            self.draw_faces.append(draw_this_face)
            if draw_this_face:
                for vertex in face:
                    self.draw_vertex[vertex] = True

obj = Object(150, 150, 150, 150, 60, 100, 6)
