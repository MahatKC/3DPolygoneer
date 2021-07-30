from Matrices.prism import create_prism
import time
import numpy as np

def normalize(x): 
    return np.any(x>200)

sides = 20
vertices = create_prism(150, 150, 150, 150, 60, 100, sides)

tzinho=time.time()

#cada coluna tem uma face, as rows representam os vertices dela
#side_faces = np.zeros((4,sides))
#vertical_faces = np.zeros((sides,2))
draw_faces = np.zeros((sides+2),dtype=bool)
#vertexFaces = np.zeros((3,sides*2))
draw_vertex = np.zeros((sides*2),dtype=bool)

arange_vector = np.arange(sides)
arange_vector_mod = (arange_vector+1)%sides
side_faces = np.stack((arange_vector,
                       arange_vector_mod,
                       arange_vector_mod+sides,
                       arange_vector+sides),
                      axis=0)

vertical_faces = np.stack((arange_vector,arange_vector+sides),axis=0)

bigger_arange = np.arange(sides*2)
#i % sides, (i + sides - 1) % sides, np.floor(i / sides) + sides
vertexFaces = np.stack((bigger_arange%sides,
                       (bigger_arange+sides-1)%sides,
                       np.floor(bigger_arange/sides)+sides
                       ),axis=0)



t0=time.time()
#vertices_em_rodem = vertices[:,side_faces[:,:2]]
#print(vertices_em_rodem)
#vertices_em_3D = np.reshape(vertices_em_rodem,(2,4,4))
#print(vertices_em_3D)

for i in range(sides):
    x = vertices[:,side_faces[:,i]]
    #print(x)
    draw_faces[i]=normalize(x)
    if normalize(x):
        draw_vertex[side_faces[:,i]]= True

#print(draw_vertex)
#print(draw_faces)

go_to_pipeline = vertices[:,draw_vertex]
#print(go_to_pipeline)
t1=time.time()
print(f"{round((t1-t0)*1000,6)} ms")
print(f"{round((t1-tzinho)*1000,6)} ms")


"""
for i in range(0, sides):
    faces.append([i, (i + 1) % sides, ((i + 1) % sides) + sides , i + sides])
    #print(faces)
#print(faces)
#faces[sides] = tuple(np.arange(sides))
arangezinh = np.arange(sides)
faces.append(arangezinh.tolist())
#faces[sides + 1] = tuple(np.arange(sides) + sides)
faces.append((arangezinh+sides).tolist())
#print(faces)
        
for i in range (0, sides * 2):
    vertexFaces.append([i % sides, (i + sides - 1) % sides, np.floor(i / sides) + sides])
    draw_vertex.append(False)

t0=time.time()
for i in range(sides+2):
    vertices_desejados = faces[i]
    x = vertices[:,vertices_desejados]
    draw_this_face = normalize(i)
    draw_faces.append(draw_this_face)
    if draw_this_face:
        for vert in vertices_desejados:
            if draw_vertex[vert]==False:
                draw_vertex[vert]= True

go_to_pipeline = vertices[:,draw_vertex]
t1=time.time()
print(f"{round((t1-tzinho)*1000,6)} ms")
"""