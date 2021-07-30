from DataStructure import Object
from Matrices.pipeline import VRP_and_n
import numpy as np

def normal_test(faces, n):    
    v1 = faces[1]
    N = np.cross(faces[0]-v1,faces[2]-v1)
    N_ = N/(np.linalg.norm(N))
    
    return np.dot(N_,n)>0

obj = Object(150, 150, 150, 150, 60, 100, 6)
for face in obj.faces:
    face_vertices = []
    for i in range(3):
        face_vertices.append(obj.vertex[:,face[i]][:3])
    break

VRP,n = VRP_and_n(50, 15, 30, 20, 6, 15)
print(normal_test(face_vertices, n))
