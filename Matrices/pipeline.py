import numpy as np
import time
from Matrices.prism import create_prism

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

def jp_times_proj_matrix(Xmin, Xmax, Ymin, Ymax, Umax, Umin, Vmax, Vmin, dist_projecao):
    u_by_x = (Umax-Umin)/(Xmax-Xmin)
    v_by_y = (Vmax-Vmin)/(Ymax-Ymin)

    minus_inverted_dp = -(1/dist_projecao)
    if is_perspectiva:
        jp_times_proj = np.zeros((4,4))
        jp_times_proj[0,0] = u_by_x
        jp_times_proj[1,1] = -v_by_y
        jp_times_proj[0,2] = (-(Xmin*u_by_x)+Umin)*minus_inverted_dp
        jp_times_proj[1,2] = ((Ymin*v_by_y)+Vmax)*minus_inverted_dp
        jp_times_proj[2,2] = 1
        jp_times_proj[3,2] = minus_inverted_dp
    else:
        jp = np.eye(4)
        jp[0,0] = u_by_x
        jp[1,1] = -v_by_y
        jp[0,3] = -(Xmin*u_by_x)+Umin
        jp[1,3] = (Ymin*v_by_y)+Vmax



def pipeline_full(M, VRPx, VRPy, VRPz, Px, Py, Pz, Yx, Yy, Yz, 
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
    u = np.cross(v,n)

    SRC = np.zeros((4,4))
    SRC[0,:3] = u
    SRC[1,:3] = v
    SRC[2,:3] = n
    SRC[0,3] = -np.dot(VRP,u)
    SRC[1,3] = -np.dot(VRP,v)
    SRC[2,3] = -np.dot(VRP,n)
    SRC[3,3] = 1

    M_in_SRC = np.dot(SRC, M)

    draw = np.any(np.logical_or(
                    np.less(M_in_SRC[2,:],-dist_near),
                    np.greater(M_in_SRC[2,:],-dist_far)
                ))

    u_by_x = (Umax-Umin)/(Xmax-Xmin)
    v_by_y = (Vmax-Vmin)/(Ymax-Ymin)

    if not draw:
        return draw, np.zeros((4,1))
    elif is_perspectiva:
        minus_inverted_dp = -(1/dist_projecao)

        jp_times_proj = np.zeros((4,4))
        jp_times_proj[0,0] = u_by_x
        jp_times_proj[1,1] = -v_by_y
        jp_times_proj[0,2] = (-(Xmin*u_by_x)+Umin)*minus_inverted_dp
        jp_times_proj[1,2] = ((Ymin*v_by_y)+Vmax)*minus_inverted_dp
        jp_times_proj[2,2] = 1
        jp_times_proj[3,2] = minus_inverted_dp

        pipelinedM = np.dot(jp_times_proj,M_in_SRC)
    else:
        jp = np.eye(4)
        jp[0,0] = u_by_x
        jp[1,1] = -v_by_y
        jp[0,3] = -(Xmin*u_by_x)+Umin
        jp[1,3] = (Ymin*v_by_y)+Vmax

        pipelinedM = np.dot(jp,M_in_SRC)
    
    pipelinedM[0,:] /= pipelinedM[3,:]
    pipelinedM[1,:] /= pipelinedM[3,:]
    pipelinedM[3,:] /= pipelinedM[3,:]

    return draw, pipelinedM

def pipeline_steps(M, VRPx, VRPy, VRPz, Px, Py, Pz, Yx, Yy, Yz, 
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
    u = np.cross(v,n)

    SRC = np.zeros((4,4))
    SRC[0,:3] = u
    SRC[1,:3] = v
    SRC[2,:3] = n
    SRC[0,3] = -np.dot(VRP,u)
    SRC[1,3] = -np.dot(VRP,v)
    SRC[2,3] = -np.dot(VRP,n)
    SRC[3,3] = 1

    M_in_SRC = np.dot(SRC, M)

    draw = np.any(np.logical_or(
                    np.less(M_in_SRC[2,:],-dist_near),
                    np.greater(M_in_SRC[2,:],-dist_far)
                ))

    if not draw:
        return draw, np.zeros((4,1))
    else:
        pipelinedM = np.dot(jp_times_proj_matrix(),M_in_SRC)
        
        pipelinedM[0,:] /= pipelinedM[3,:]
        pipelinedM[1,:] /= pipelinedM[3,:]
        pipelinedM[3,:] /= pipelinedM[3,:]

        return draw, pipelinedM

def pipeline3(M, VRPx, VRPy, VRPz, Px, Py, Pz, Yx, Yy, Yz, 
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
    N = VRP-np.array([Px, Py, Pz])
    n = N/(np.linalg.norm(N))

    z_row = np.dot(n,M[0:3,:])-np.dot(VRP,n)

    draw = np.any(np.logical_or(
                    np.less(z_row,-dist_near),
                    np.greater(z_row,-dist_far)
                ))

    if not draw:
        return draw, np.zeros((4,1))
    else:
        Y = np.array([Yx, Yy, Yz])
        V = Y-np.dot(np.dot(Y,n),n)
        v = V/(np.linalg.norm(V))
        u = np.cross(v,n)

        VRP_n = np.dot(VRP,n)

        u_by_x = (Umax-Umin)/(Xmax-Xmin)
        v_by_y = (Vmax-Vmin)/(Ymax-Ymin)

        if is_perspectiva:
            minus_inverted_dp = -(1/dist_projecao)
            alfa = (-(Xmin*u_by_x)+Umin)*minus_inverted_dp
            beta = ((Ymin*v_by_y)+Vmax)*minus_inverted_dp

            pipeline_matrix = np.zeros((4,4))
            pipeline_matrix[0,0:3] = (u_by_x*u)+(n*alfa)
            pipeline_matrix[1,0:3] = (-v_by_y*v)+(n*beta)
            pipeline_matrix[2,0:3] = n 
            pipeline_matrix[3,0:3] = minus_inverted_dp*n
            pipeline_matrix[0,3] = -(np.dot(VRP,u)*u_by_x)-(alfa*VRP_n)
            pipeline_matrix[1,3] = (np.dot(VRP,v)*v_by_y)-(beta*VRP_n)
            pipeline_matrix[2,3] = -VRP_n
            pipeline_matrix[3,3] = -VRP_n*minus_inverted_dp

            pipelinedM = np.dot(pipeline_matrix,M)
        else:
            alfa = -(Xmin*u_by_x)+Umin
            beta = (Ymin*v_by_y)+Vmax

            pipeline_matrix = np.zeros((4,4))
            pipeline_matrix[0,0:3] = (u_by_x*u)+(n*alfa)
            pipeline_matrix[1,0:3] = (-v_by_y*v)+(n*beta)
            pipeline_matrix[2,0:3] = n
            pipeline_matrix[0,3] = -(np.dot(VRP,u)*u_by_x)+alfa
            pipeline_matrix[1,3] = (np.dot(VRP,v)*v_by_y)+beta
            pipeline_matrix[2,3] = -VRP_n
            pipeline_matrix[3,3] = 1

            pipelinedM = np.dot(pipeline_matrix,M)
        
        pipelinedM[0,:] /= pipelinedM[3,:]
        pipelinedM[1,:] /= pipelinedM[3,:]
        pipelinedM[3,:] /= pipelinedM[3,:]

        return draw, pipelinedM

poliedro_teste = np.array([[30, 35, 25, 20,   30],
                           [ 2,  4,  3,  1,   10],
                           [25, 20, 18, 23, 22.5],
                           [ 1,  1,  1,  1,    1]])

draw, R = pipeline3(poliedro_teste, 50, 15, 30, 20, 6, 15, 0, 1, 0, 10, 40, True, 17, -8, 8, -5, 5, 320, 0, 240, 0)

"""
t_ms=round((t1-t0),6)
print(f"{t_ms*1000} ms")
print(f"{round(1/(t_ms),3)} FPS") 
"""