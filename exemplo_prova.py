from DataStructure.normal_test import normal_test
from DataStructure.Matrices.pipeline import pipeline_steps
from DataStructure.Matrices.transforms import scale
import numpy as np

class exemplo_prova():
    def __init__(self):
        self.prism_in_SRU = np.array([[-10.868, -7.001, -5.67,   3.98,  7.847,  9.178],
                                      [   1.64,   5.736, 9.832, -9.832, -5.736,  -1.64],
                                      [  2.861,   4.368, 0.437, -4.062, -2.556, -6.487],
                                      [      1,       1,     1,      1,      1,     1,]])
        self.prism_in_SRT = None
        self.draw_me = None
        self.faces = []
        self.draw_faces = []
        self.vertexFaces = []
        self.draw_vertex = [False]*6
        self.numberFaces = 5
        self.sides = 3
        sides=3

        sides_minus_one = 5
        self.faces.append([0,3,4,1])
        self.faces.append([1,4,5,2])
        self.faces.append([2,5,3,0])
        self.faces.append(np.arange(sides).tolist())
        self.faces.append([3,5,4])
        
        self.vertexFaces.append([0,2,3])
        self.vertexFaces.append([1,0,3])
        self.vertexFaces.append([2,1,3])
        self.vertexFaces.append([2,0,4])
        self.vertexFaces.append([1,2,4])
        self.vertexFaces.append([0,1,4])

    def printa_tudo(self):
        print("Faces list: ")
        print(self.faces)
        print("-"*10)
        print("Vertices list: ")
        print(self.vertexFaces)
        print("-"*10)

    def getCoordinates(self, face_SRU):
        list = []
        for i in range(len(self.faces[face_SRU])):
            vertex_in_SRU = self.faces[face_SRU][i]
            vertex_in_SRT = np.arange(self.sides * 2)[self.draw_vertex].tolist().index(vertex_in_SRU)
            list.append(int(self.prism_in_SRT[0][vertex_in_SRT]))
            list.append(int(self.prism_in_SRT[1][vertex_in_SRT]))     
        return list
    """
    def getCoordinates(self, face_SRU):
        list = []
        for i in range(len(self.faces[face_SRU])):
            list.append(int(self.prism_in_SRU[0][self.faces[face_SRU][i]]))
            list.append(int(self.prism_in_SRU[1][self.faces[face_SRU][i]]))
        return list

    def getCoordinates(self, face_SRU):
        list = []
        for i in range(len(self.faces[face_SRU])):
            list.append(int(self.prism_in_SRT[0][i]))
            list.append(int(self.prism_in_SRT[1][i]))     
        return list
    """ 

    def normalVisualizationTest(self, n):
        for face in self.faces:
            face_vertices = []
            print(face)
            for i in range(3):
                face_vertices.append(self.prism_in_SRU[:3,face[i]])
            draw_this_face = normal_test(face_vertices, n)
            self.draw_faces.append(draw_this_face)
            if draw_this_face:
                for vertex in face:
                    self.draw_vertex[vertex] = True

    def pipeline_me(self, SRC_matrix, jp_proj_matrix, dist_near, dist_far):
        self.draw_me, self.prism_in_SRT = pipeline_steps(self.prism_in_SRU[:,self.draw_vertex], SRC_matrix, jp_proj_matrix, dist_near, dist_far)
