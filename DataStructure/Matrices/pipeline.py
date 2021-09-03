import numpy as np

def VRP_and_n(VRPx, VRPy, VRPz, Px, Py, Pz):
    VRP = np.array([VRPx, VRPy, VRPz])
    N = VRP-np.array([Px, Py, Pz])
    n = N/(np.linalg.norm(N))

    return VRP,n

def SRC_matrix(VRP, n, Yx, Yy, Yz):
    """Returns the transformation matrix to change the prism from SRU coordinates
    to SRC. 
    Args: VRP coordinates, P coordinates, View-up (Y) coordinates"""
    
    Y = np.array([Yx, Yy, Yz])
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

def jp_times_proj_matrix(is_perspectiva, dist_projecao, 
    Xmin, Xmax, Ymin, Ymax, Umax, Umin, Vmax, Vmin):
    """Returns a matrix used to transform an object from SRC to SRT."""

    u_by_x = (Umax-Umin)/(Xmax-Xmin)
    v_by_y = (Vmax-Vmin)/(Ymax-Ymin)

    if is_perspectiva:
        minus_inverted_dp = -(1/dist_projecao)
        jp_times_proj = np.zeros((4,4))
        jp_times_proj[0,0] = u_by_x
        jp_times_proj[1,1] = -v_by_y
        jp_times_proj[0,2] = (-(Xmin*u_by_x)+Umin)*minus_inverted_dp
        jp_times_proj[1,2] = ((Ymin*v_by_y)+Vmax)*minus_inverted_dp
        jp_times_proj[2,2] = 1
        jp_times_proj[3,2] = minus_inverted_dp

        return jp_times_proj
    else:
        jp = np.eye(4)
        jp[0,0] = u_by_x
        jp[1,1] = -v_by_y
        jp[0,3] = -(Xmin*u_by_x)+Umin
        jp[1,3] = (Ymin*v_by_y)+Vmax

        return jp 

def pipeline_steps(M, SRC_matrix, jp_proj_matrix, dist_near, dist_far):
    """
    Returns a Boolean value determining if the object should be drawn
    and a numpy array for the prism after the application of the pipeline.
    Args:
    M is the numpy array for the prism to be drawn.
    SRC_matrix and jp_proj_matrix are the matrices returned from the first_pipeline function.
    dist_near and dist_fear determine the Z limits of the scene.
    """
    M_in_SRC = np.dot(SRC_matrix, M)
    
    draw = np.all(np.logical_and(
                    np.less(M_in_SRC[2,:],-dist_near),
                    np.greater(M_in_SRC[2,:],-dist_far)
                ))

    if not draw:
        return draw, np.zeros((4,1))
    else:
        pipelinedM = np.dot(jp_proj_matrix, M_in_SRC)
        
        pipelinedM[0,:] /= pipelinedM[3,:]
        pipelinedM[1,:] /= pipelinedM[3,:]
        pipelinedM[3,:] /= pipelinedM[3,:]

        return draw, pipelinedM

def first_pipeline(VRP, n, Yx, Yy, Yz, 
    is_perspectiva, dist_projecao, 
    Xmin, Xmax, Ymin, Ymax, Umin, Umax, Vmin, Vmax):
    """Returns matrices that shall be used in the pipeline based on all the parameters necessary
    for the SRU to SRT conversion, except the 3D cut step."""
        
    SRC = SRC_matrix(VRP, n, Yx, Yy, Yz)
    jp_times_proj = jp_times_proj_matrix(is_perspectiva, dist_projecao, 
    Xmin, Xmax, Ymin, Ymax, Umax, Umin, Vmax, Vmin)

    return SRC, jp_times_proj