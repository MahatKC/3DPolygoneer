from DataStructure.normal_test import normal_test
from DataStructure.Matrices.prism import create_prism
from DataStructure.Matrices.pipeline import SRC_matrix, pipeline_steps
from DataStructure.Matrices.transforms import translation, scaleAlongAxis, rotXAlongAxis, rotYAlongAxis, rotZAlongAxis
#from normal_test import normal_test
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
        self.prism_in_SRU = create_prism(x, y, z, h, r_bottom, r_top, sides)
        self.prism_in_SRT = None
        self.draw_me = None
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
            floor = int(np.floor(v/sides))
            self.vertexFaces.append([v%sides, (sides*(1+floor))-v-1, floor+sides])
    
    def printa_tudo(self):
        print("Faces list: ")
        print(self.faces)
        print("-"*10)
        print("Vertices list: ")
        print(self.vertexFaces)
        print("-"*10)

    def translation(self, valueX, valueY, valueZ):
        self.prism_in_SRU = translation(self.prism_in_SRU, valueX, valueY, valueZ)
        

    def getCoordinates(self, face_SRU):
        list = []
        for i in range(len(self.faces[face_SRU])):
            vertex_in_SRU = self.faces[face_SRU][i]
            vertex_in_SRT = np.arange(self.sides * 2)[self.draw_vertex].tolist().index(vertex_in_SRU)
            list.append(int(self.prism_in_SRT[0][vertex_in_SRT]))
            list.append(int(self.prism_in_SRT[1][vertex_in_SRT]))     
        return list

    def normalVisualizationTest(self, n):
        for face in self.faces:
            face_vertices = []
            for i in range(3):
                face_vertices.append(self.prism_in_SRU[:3,face[i]])
            draw_this_face = normal_test(face_vertices, n)
            self.draw_faces.append(draw_this_face)
            if draw_this_face:
                for vertex in face:
                    self.draw_vertex[vertex] = True

    def pipeline_me(self, SRC_matrix, jp_proj_matrix, dist_near, dist_far):
        self.draw_me, self.prism_in_SRT = pipeline_steps(self.prism_in_SRU[:,self.draw_vertex], SRC_matrix, jp_proj_matrix, dist_near, dist_far)


obj = Object(150, 150, 150, 150, 60, 100, 6)
obj.printa_tudo()

