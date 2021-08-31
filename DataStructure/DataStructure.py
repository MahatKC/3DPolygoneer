from DataStructure.Matrices.sombreamento_constante import sombreamento_constante
from DataStructure.normal_test import normal_test
from DataStructure.Matrices.prism import create_prism
from DataStructure.Matrices.pipeline import pipeline_steps
from DataStructure.Matrices.transforms import translation, scaleAlongAxis, rotXAlongAxis, rotYAlongAxis, rotZAlongAxis
import numpy as np
import copy
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)

class Object():
    def __init__(self, x, y, z, h, r_bottom, r_top, sides, ka, kd, ks, n):
        self.r_bottom = r_bottom
        self.r_top = r_top
        self.height = h
        self.sides = sides
        
        self.prism_in_SRU = create_prism(x, y, z, h, r_bottom, r_top, sides)
        self.prism_in_SRT = None
        self.normal_of_faces = []
        self.normal_of_viewPort_faces = []
        self.color_of_faces = []
        self.zeroed_SRT = None
        self.viewport_faces = []
        self.draw_me = None
        self.faces = []
        self.draw_faces = []
        self.vertexFaces = []
        self.draw_vertex = [False]*sides*2
        self.numberFaces = sides + 2
        self.ka = ka 
        self.kd = kd 
        self.ks = ks 
        self.n = n
        sides_minus_one = sides*2-1
        for f in range(0, sides):
            complement_of_next = (f+1)%sides
            self.faces.append([f, sides_minus_one-f, sides_minus_one-complement_of_next, complement_of_next])
        self.faces.append(np.arange(sides).tolist())
        self.faces.append((np.arange(sides) + sides).tolist())
        
        for v in range(0, sides*2):
            floor = int(np.floor(v/sides))
            self.vertexFaces.append([v%sides, (sides*(1+floor))-v-1, floor+sides])
    
    def translation(self, valueX, valueY, valueZ):
        self.prism_in_SRU = translation(self.prism_in_SRU, valueX, valueY, valueZ)

    def scale(self, Sx, Sy, Sz):
        self.prism_in_SRU = scaleAlongAxis(self.prism_in_SRU, Sx, Sy, Sz)

    def rotationX(self, rotationValue):
        self.prism_in_SRU = rotXAlongAxis(self.prism_in_SRU, rotationValue)

    def rotationY(self, rotationValue):
        self.prism_in_SRU = rotYAlongAxis(self.prism_in_SRU, rotationValue)

    def rotationZ(self, rotationValue):
        self.prism_in_SRU = rotZAlongAxis(self.prism_in_SRU, rotationValue)    

    def getCoordinates(self, viewport_face_idx):
        list = []
        for i in range(np.shape(self.viewport_faces[viewport_face_idx])[1]):
            list.append(round(self.viewport_faces[viewport_face_idx][0,i]))
            list.append(round(self.viewport_faces[viewport_face_idx][1,i]))     
        return list

    def normalVisualizationTest(self, n):
        self.draw_vertex = [False]*self.sides*2
        self.draw_faces.clear()
        self.normal_of_faces.clear()
        for face in self.faces:
            face_vertices = []
            for i in range(3):
                face_vertices.append(self.prism_in_SRU[:3,face[i]])
            draw_this_face, normal_of_this_face = normal_test(face_vertices, n)
            self.normal_of_faces.append(normal_of_this_face)
            self.draw_faces.append(draw_this_face)
            if draw_this_face:
                for vertex in face:
                    self.draw_vertex[vertex] = True

    def pipeline_me(self, SRC_matrix, jp_proj_matrix, dist_near, dist_far):
        self.draw_me, self.prism_in_SRT = pipeline_steps(self.prism_in_SRU[:,self.draw_vertex], SRC_matrix, jp_proj_matrix, dist_near, dist_far)
    
    def sombreamento_constante(self, VRP, il, ila, fonte_luz):
        self.color_of_faces = sombreamento_constante(self.viewport_faces, self.normal_of_viewPort_faces, VRP, self.ka, self.kd, self.ks, self.n, il, ila, fonte_luz)

    def crop_to_screen(self, u_min, u_max, v_min, v_max):
        self.zeroed_SRT = np.zeros((4,self.sides*2))+np.array([[u_min],[v_min],[0],[0]])
        self.zeroed_SRT[:,self.draw_vertex] = self.prism_in_SRT[:,:]
        self.viewport_faces = []
        self.normal_of_viewPort_faces.clear()
        for i in range(self.numberFaces):
            if self.draw_faces[i]:
                self.normal_of_viewPort_faces.append(self.normal_of_faces[i])
                face = self.faces[i]
                new_viewport_face = self.sutherland_hodgeman(face, u_min, u_max, v_min, v_max) 
                if np.shape(new_viewport_face)[1] != 0:
                    self.viewport_faces.append(new_viewport_face)
 
    def get_boolean_mask(self, face_vertices, borders):
        v0 = face_vertices[0,:]<borders[0]
        v1 = face_vertices[0,:]>borders[1]
        v2 = face_vertices[1,:]>borders[2]
        v3 = face_vertices[1,:]<borders[3]
        vfinal = np.any((v0,v1,v2,v3),axis=0)
        boolean_mask = np.stack((v0,v1,v2,v3,vfinal),axis=0)

        return boolean_mask
    
    def sutherland_hodgeman(self, face, u_min, u_max, v_min, v_max):
        v0 = self.zeroed_SRT[0,face]<u_min
        v1 = self.zeroed_SRT[0,face]>u_max
        v2 = self.zeroed_SRT[1,face]>v_max
        v3 = self.zeroed_SRT[1,face]<v_min
        vfinal = np.any((v0,v1,v2,v3),axis=0)
        boolean_mask = np.stack((v0,v1,v2,v3,vfinal),axis=0)
   
        face_vertices = copy.deepcopy(self.zeroed_SRT[:,face])

        borders = [u_min, u_max, v_max, v_min]
        len_face = len(face)

        for viewport_edge in range(4):            
            if np.any(boolean_mask[viewport_edge,:]):
                new_face_vertices = np.empty((4,0))

                for i in range(len_face):
                    j=(i+1)%len_face
                    v1_idx = i
                    v2_idx = j
                    v1_out = boolean_mask[viewport_edge,i]
                    v2_out = boolean_mask[viewport_edge,j]

                    if v1_out!=v2_out:
                        if v1_out:
                            new_vertex=self.get_intersection_coordinate(face_vertices[:,v1_idx], face_vertices[:,v2_idx], viewport_edge<2, borders[viewport_edge])
                            new_face_vertices=np.append(new_face_vertices,new_vertex,axis=1)
                            new_face_vertices=np.append(new_face_vertices,face_vertices[:,v2_idx][:,np.newaxis],axis=1)
                        else:
                            new_vertex=self.get_intersection_coordinate(face_vertices[:,v2_idx], face_vertices[:,v1_idx], viewport_edge<2, borders[viewport_edge])
                            new_face_vertices=np.append(new_face_vertices,new_vertex,axis=1)
                            
                    else:
                        if v1_out==0:
                            new_face_vertices=np.append(new_face_vertices,face_vertices[:,v2_idx][:,np.newaxis],axis=1)

                face_vertices=new_face_vertices
                len_face = np.shape(new_face_vertices)[1]
                boolean_mask=self.get_boolean_mask(face_vertices, borders)

        return face_vertices

    def get_intersection_coordinate(self, vert1, vert2, is_border_vertical, border_value):
        x1 = vert1[0]
        y1 = vert1[1]
        z1 = vert1[2]
        x2 = vert2[0]
        y2 = vert2[1]
        z2 = vert2[2]
        y2_min_y1 = y2-y1
        x2_min_x1 = x2-x1
        z2_min_z1 = z2-z1

        if is_border_vertical:
            x = border_value
            u = (border_value-x1)/x2_min_x1
            y = u*y2_min_y1+y1

        else:
            y = border_value
            u = (border_value-y1)/y2_min_y1
            x = u*x2_min_x1+x1
        
        z = z1+u*z2_min_z1

        return np.array([[x],[y],[z],[1]])
    
    def FacesOrder(self):
        if len(self.viewport_faces) > 0:
            z_values = [np.min(face[2,:]) for face in self.viewport_faces]
            self.faces_order = np.argsort(z_values)
            self.object_min_z = np.min(z_values)
        else:
            self.faces_order = []
            self.object_min_z = 0