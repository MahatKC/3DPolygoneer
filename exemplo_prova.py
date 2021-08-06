from DataStructure.normal_test import normal_test
from DataStructure.Matrices.pipeline import pipeline_steps
import numpy as np

class exemplo_prova():
    def __init__(self):
        self.prism_in_SRU = np.array([[-10.868, -70.001, -5.67,   3.98,  7.847,  9.178],
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
        for f in range(0, sides):
            complement_of_next = (f+1)%sides
            self.faces.append([f, sides_minus_one-f, sides_minus_one-complement_of_next, complement_of_next])
        self.faces.append(np.arange(sides).tolist())
        self.faces.append((np.arange(sides) + sides).tolist())
        
        for v in range(0, sides*2):
            floor = int(np.floor(v/sides))
            self.vertexFaces.append([v%sides, (sides*(1+floor))-v-1, floor+sides])

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