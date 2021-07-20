import numpy as np
import time
from prism import create_prism

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

def SRU_to_SRC_matrix(VRPx, VRPy, VRPz, Px, Py, Pz, Yx, Yy, Yz):
    """Returns the transformation matrix to change the prism from SRU coordinates
    to SRC. 
    Args: VRP coordinates, P coordinates, View-up (Y) coordinates"""
    
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

def did_cut_3D_happen(M,dist_near,dist_far):
    """Returns if a prism will be drawn or not based on the 3D Cut.
    Args:
    Matrix M after SRC transformation, distance to nearest plane and distance to furthest plane."""
    avg = np.average(M, axis=1)
    z = avg[2]
    return z>-dist_near or z<-dist_far

def projection_matrix(is_perspectiva,dist_projecao):
    """Returns the matrix for the projection transformation based on the user's defined
    projection type.
    Args:
    Boolean variable is_perspectiva, dist_projecao that is only used for perspective projection.
    """
    M = np.eye(4)
    if is_perspectiva:
        M[3,3]=0
        M[3,2]=-(1/dist_projecao)
    return M
        
def SRC_to_SRT_matrix(Xmin,Xmax,Ymin,Ymax,Umax,Umin,Vmax,Vmin):
    """Returns matrix to transform prism in SRC to SRT.
    Args: X, Y, U and V values."""
    
    u_by_x = (Umax-Umin)/(Xmax-Xmin)
    v_by_y = (Vmax-Vmin)/(Ymax-Ymin)
    M = np.eye(4)
    M[0,0] = u_by_x
    M[1,1] = -v_by_y
    M[0,3] = -(Xmin*u_by_x)+Umin
    M[1,3] = (Ymin*v_by_y)+Vmax
    
    return M

def pipeline(M, VRPx, VRPy, VRPz, Px, Py, Pz, Yx, Yy, Yz, 
    dist_near, dist_far, is_perspectiva, dist_projecao, 
    Xmin, Xmax, Ymin, Ymax, Umax, Umin, Vmax, Vmin):
    """
    Returns a Boolean value determining if the object should be drawn
    and a numpy array for the prism after the application of the pipeline.
    Args:
    M is the numpy array for the prism to be drawn.
    VRPx, VRPy, VRPz, Px, Py, Pz, Yx, Yy, Yz
    M, dist_near, dist_far
    is_perspectiva, dist_projecao
    Xmin, Xmax, Ymin, Ymax, Umax, Umin, Vmax, Vmin
    """
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

    avg = np.average(M, axis=1)
    z = avg[2]
    draw = (z>-dist_near or z<-dist_far)

    if not draw:
        return draw, np.zeros((4,1))
    else:
        proj = np.eye(4)
        if is_perspectiva:
            proj[3,3]=0
            proj[3,2]=-(1/dist_projecao)
    
        u_by_x = (Umax-Umin)/(Xmax-Xmin)
        v_by_y = (Vmax-Vmin)/(Ymax-Ymin)
        jp = np.eye(4)
        jp[0,0] = u_by_x
        jp[1,1] = -v_by_y
        jp[0,3] = -(Xmin*u_by_x)+Umin
        jp[1,3] = (Ymin*v_by_y)+Vmax

        pipelinedM = np.dot(np.dot(np.dot(jp,proj),SRC),M)
        pipelinedM[0,:] /= pipelinedM[3,:]
        pipelinedM[1,:] /= pipelinedM[3,:]
        pipelinedM[3,:] /= pipelinedM[3,:]

        return draw, pipelinedM

F = create_prism(1,2,-6,4,5,6,7)

poliedro_teste = np.array([[30, 35, 25, 20,   30],
                           [ 2,  4,  3,  1,   10],
                           [25, 20, 18, 23, 22.5],
                           [ 1,  1,  1,  1,    1]])

t0 = time.time()
draw, R = pipeline(poliedro_teste, 50, 15, 30, 20, 6, 15, 0, 1, 0, 10, 40, True, 17, -8, 8, -5, 5, 320, 0, 240, 0)
t1 = time.time()
print(t1-t0)
