from DataStructure import Object
import numpy as np
def normal_test(faces):
    v0 = faces[0]
    v1 = faces[1]
    v2 = faces[2]
    print(v0)
    print(v1)
    print(v2)
    print(type(v0))

    pass

obj = Object(150, 150, 150, 150, 60, 100, 6)
for face in obj.faces:
    face_vertices = []
    for i in range(3):
        face_vertices.append(obj.vertex[:,face[i]])

normal_test(face_vertices)

print(obj.faces)
print(obj.vertexFaces)
print(obj.vertex)