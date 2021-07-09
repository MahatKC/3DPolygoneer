import numpy as np
from prism import prism, vertices

def translation(M, dx, dy, dz):
    """Translates all vertices from M according to the coordinates dx, dy and dz.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    T[0,3] = dx
    T[1,3] = dy
    T[2,3] = dz
    return np.dot(T,M)

def scale(M, Sx, Sy, Sz):
    """Scales polygon M by Sx, Sy and Sz.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    T[0,0] = Sx
    T[1,1] = Sy
    T[2,2] = Sz
    return np.dot(T,M)

def rotX(M, alpha):
    """Rotates polygon M around X axis by alpha degrees.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    alpha_radians = np.radians(alpha)
    sin = np.sin(alpha_radians)
    cos = np.cos(alpha_radians)
    T[1,1] = cos
    T[2,2] = cos
    T[1,2] = -sin
    T[2,1] = sin
    return np.dot(T,M)

def rotZ(M, alpha):
    """Rotates polygon M around Z axis by alpha degrees.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    alpha_radians = np.radians(alpha)
    sin = np.sin(alpha_radians)
    cos = np.cos(alpha_radians)
    T[0,0] = cos
    T[1,1] = cos
    T[0,1] = -sin
    T[1,0] = sin
    return np.dot(T,M)

def rotY(M, alpha):
    """Rotates polygon M around Y axis by alpha degrees.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    alpha_radians = np.radians(alpha)
    sin = np.sin(alpha_radians)
    cos = np.cos(alpha_radians)
    T[0,0] = cos
    T[2,2] = cos
    T[0,2] = sin
    T[2,0] = -sin
    return np.dot(T,M)

def rotYAlongAxis(M, alpha):
    """Rotates polygon M around the polygon's own Y axis by alpha degrees.
    This translates the polygon, rotates it and then translates it back.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    alpha_radians = np.radians(alpha)
    sin = np.sin(alpha_radians)
    cos = np.cos(alpha_radians)
    T[0,0] = cos
    T[1,1] = cos
    T[0,1] = -sin
    T[1,0] = sin
    return np.dot(T,M) 

F = prism(1,2,3,4,5,6,20)
upper_vertices = vertices(F.sides, F.r_bottom, F.center_bottom)
print(upper_vertices)
print("-"*20)
print(translation(upper_vertices,-7,0,-3))