import numpy as np
import time
from prism import create_prism

def SRU_to_SRC(VRPx, VRPy, VRPz, Px, Py, Pz, Yx, Yy, Yz):
    VRP = np.array([VRPx, VRPy, VRPz])
    Y = np.array([Yx, Yy, Yz])
    N = VRP-np.array([Px, Py, Pz])
    n = N/(np.linalg.norm(N))
    V = Y-np.dot(np.dot(Y,n),n)
    v = V/(np.linalg.norm(V))
    SRC = np.eye(4)
    u = np.cross(v,n)
    SRC[0,:3] = u
    SRC[1,:3] = v
    SRC[2,:3] = n
    SRC[0,3] = -np.dot(VRP,u)
    SRC[1,3] = -np.dot(VRP,v)
    SRC[2,3] = -np.dot(VRP,n)

    return SRC

def pipeline(VRP,P,Y,dist_near,dist_far,is_perspectiva,dist_projecao,Xmin,Xmax,Ymin,Ymax,Umax,Umin,Vmax,Vmin):

    
    pass
"""
Variáveis:
VRP -> VRP
P -> P
Vetor View-up -> Y
Distancia do plano Near -> n
Distancia do plano Far -> f
Tipo de projeção (paralela axonométrica/perspectiva) -> Matriz de projeção
Distancia ao plano de projeção -> dp
Limites do mundo -> Xmin, Xmax, Ymin, Ymax
Limites do plano de projeção -> Umax, Umin, Vmax, Vmin
"""

VRPx=4
VRPy=3
VRPz=2
Px=3
Py=2
Pz=1
Yx=1
Yy=2
Yz=1

t0=time.time()
SRU_to_SRC(VRPx, VRPy, VRPz, Px, Py, Pz, Yx, Yy, Yz)
t1=time.time()

print(t1-t0)
