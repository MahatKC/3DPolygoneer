#from normal_test import normal_test
#from Matrices.prism import create_prism
#from Matrices.pipeline import VRP_and_n, first_pipeline, pipeline_steps
from DataStructure.normal_test import normal_test
from DataStructure.Matrices.prism import create_prism
from DataStructure.Matrices.pipeline import  VRP_and_n, first_pipeline, SRC_matrix, pipeline_steps
from DataStructure.Matrices.transforms import translation, scaleAlongAxis, rotXAlongAxis, rotYAlongAxis, rotZAlongAxis
import numpy as np
import copy
np.set_printoptions(precision=6)
np.set_printoptions(suppress=True)

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
        self.r_bottom = r_bottom
        self.r_top = r_top
        self.height = h
        self.sides = sides
        
        self.prism_in_SRU = create_prism(x, y, z, h, r_bottom, r_top, sides)
        self.prism_in_SRT = None
        self.zeroed_SRT = None
        self.viewport_faces = []
        self.draw_me = None
        self.faces = []
        self.draw_faces = []
        self.vertexFaces = []
        self.draw_vertex = [False]*sides*2
        self.numberFaces = sides + 2

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
        self.draw_faces.clear()
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
    
    def crop_to_screen(self, u_min, u_max, v_min, v_max):
        self.zeroed_SRT = np.zeros((4,self.sides*2))+np.array([[u_min],[v_min],[0],[0]])
        self.zeroed_SRT[:,self.draw_vertex] = self.prism_in_SRT[:,:]
        
        v0 = self.zeroed_SRT[0,:]<u_min
        v1 = self.zeroed_SRT[0,:]>u_max
        v2 = self.zeroed_SRT[1,:]>v_max
        v3 = self.zeroed_SRT[1,:]<v_min
        vfinal = np.any((v0,v1,v2,v3),axis=0)
        boolean_mask = np.stack((v0,v1,v2,v3,vfinal),axis=0)

        for i in range(self.numberFaces):
            if self.draw_faces[i]:
                face = self.faces[i]
                len_face = len(face)
                #l1 = self.create_l1(face, len_face, boolean_mask, u_min, u_max, v_min, v_max)
                self.viewport_faces.append(self.sutherland_hodgeman(face, len_face, boolean_mask, u_min, u_max, v_min, v_max))
                
        pass

    def sutherland_hodgeman(self, face, len_face, boolean_mask, u_min, u_max, v_min, v_max):
        face_vertices = copy.deepcopy(self.zeroed_SRT)
        borders = [u_min, u_max, v_max, v_min]
        for viewport_edge in range(4):
            if np.any(boolean_mask[viewport_edge,:]):
                for i in range(len_face):
                    j=(i+1)%len_face
                    v1_idx = face[i]
                    v2_idx = face[j]

                    v1_out = boolean_mask[viewport_edge,v1_idx]
                    v2_out = boolean_mask[viewport_edge,v2_idx]

                    if v1_out!=v2_out:
                        if v1_out:
                            face_vertices[:,v1_idx] = self.get_intersection_coordinate(face_vertices[:,v1_idx], face_vertices[:,v2_idx], viewport_edge<2, borders[viewport_edge])
                            boolean_mask[viewport_edge,v1_idx]=0
                        else:
                            face_vertices[:,v2_idx] = self.get_intersection_coordinate(face_vertices[:,v2_idx], face_vertices[:,v1_idx], viewport_edge<2, borders[viewport_edge])
                            boolean_mask[viewport_edge,v2_idx]=0

        return face_vertices[:,face]

    def create_l1(self, face, len_face, boolean_mask, u_min, u_max, v_min, v_max):
        l1=[]
        for i in range(len_face):
            if i==len_face-1:
                j=0
            else:
                j=i+1

            v1_idx = face[i]
            v2_idx = face[j]
            
            l1.append(self.zeroed_SRT[:,v1_idx])
            #não estão na mesma região nem estão de um mesmo lado de fora

            if not np.array_equal(boolean_mask[:,v1_idx],boolean_mask[:,v2_idx]) and (not np.any(np.logical_and(boolean_mask[:4,v1_idx],boolean_mask[:4,v2_idx]))):
                print("entrou if")
                #um dentro, outro fora (iguais ja verificado acima)
                if boolean_mask[3,v1_idx]==0 or boolean_mask[3,v2_idx]==0:
                    point = self.get_intersection_point(boolean_mask, v1_idx, v2_idx, u_min, u_max, v_min, v_max)
                    if np.shape(point)[0]>1:
                        l1.append(point)
                #um de cada lado, fora
                else:
                    point = self.get_intersection_point(boolean_mask, v1_idx, v2_idx, u_min, u_max, v_min, v_max)
                    if np.shape(point)[0]>1:
                        l1.append(point)
                        l1.append(self.get_intersection_point(boolean_mask, v2_idx, v1_idx, u_min, u_max, v_min, v_max))

        return l1

    def get_intersection_point(self, boolean_mask, v1, v2, u_min, u_max, v_min, v_max):
        found_it = False
        if boolean_mask[0,v1]:
            intersect_point, z_value = self.get_intersection_coordinate(self.zeroed_SRT[:,v1], self.zeroed_SRT[:,v2], True, u_min)
            if intersect_point > v_min and intersect_point < v_max:
                found_it = True
                return np.array([[u_min-1],[intersect_point],[z_value],[1]])
        elif boolean_mask[1,v1] and not found_it:
            intersect_point, z_value = self.get_intersection_coordinate(self.zeroed_SRT[:,v1], self.zeroed_SRT[:,v2], True, u_max)
            print("1")
            print(intersect_point, z_value)
            if intersect_point > v_min and intersect_point < v_max:
                found_it = True
                return np.array([[u_max+1],[intersect_point],[z_value],[1]])
        elif boolean_mask[2,v1] and not found_it:
            intersect_point, z_value = self.get_intersection_coordinate(self.zeroed_SRT[:,v1], self.zeroed_SRT[:,v2], False, v_min)
            print("2")
            print(intersect_point, z_value)
            if intersect_point > u_min and intersect_point < u_max:
                found_it = True
                return np.array([[intersect_point],[v_max+1],[z_value],[1]])
        elif boolean_mask[3,v1] and not found_it:
            intersect_point, z_value = self.get_intersection_coordinate(self.zeroed_SRT[:,v1], self.zeroed_SRT[:,v2], False, v_max)
            print("3")
            print(intersect_point, z_value)
            if intersect_point > u_min and intersect_point < u_max:
                found_it = True
                return np.array([[intersect_point],[v_min-1],[z_value],[1]])
        else:
            return np.array([0])

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
            y = ((border_value-x1)*y2_min_y1/x2_min_x1)+y1
            z = z1+(z2_min_z1*y/y2_min_y1)
        else:
            x = ((border_value-y1)*x2_min_x1/y2_min_y1)+x1
            y = border_value
            z = z1 + (z2_min_z1*x/x2_min_x1)

        return np.array([x,y,z,1])


obejeto = "quadradao"

if obejeto == "quina":
    poliedro_teste = Object(0, 0, 0, 10, 10, 10, 10)
    VRP,n = VRP_and_n(0, 20, 100, 2, 1, 3)
    poliedro_teste.normalVisualizationTest(n)
    SRC_matrix, jp_proj_matrix = first_pipeline(VRP, n, 0, 1, 0, False, 50, -40, -15, -40, 15, 300, 1000, 200, 600)
    poliedro_teste.pipeline_me(SRC_matrix, jp_proj_matrix, 10, 1000)
elif obejeto=="quadradao":
    poliedro_teste = Object(0, 0, 0, 15, 15, 110, 4)
    VRP,n = VRP_and_n(0, 0, 1000, 2, 1, 3)
    poliedro_teste.normalVisualizationTest(n)
    SRC_matrix, jp_proj_matrix = first_pipeline(VRP, n, 0, 1, 0, False, 50, -50, 40, -40, 30, 300, 1000, 200, 600)
    poliedro_teste.pipeline_me(SRC_matrix, jp_proj_matrix, 10, 1000)

print(poliedro_teste.prism_in_SRT)
poliedro_teste.crop_to_screen(300, 1000, 200, 600)
print(poliedro_teste.viewport_faces)
for viewport_face_idx in range(len(poliedro_teste.viewport_faces)):
    print(poliedro_teste.getCoordinates(viewport_face_idx))
        