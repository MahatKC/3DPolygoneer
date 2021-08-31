import numpy as np

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
    
    M = translation(M,)
    T = np.eye(4)
    T[0,0] = Sx
    T[1,1] = Sy
    T[2,2] = Sz
    return np.dot(T,M)

def scaleAlongAxis(M, Sx, Sy, Sz):
    """Scales polygon M based on its geometric center by Sx, Sy and Sz."""
    T = np.zeros((4,4))
    avg = np.average(M, axis=1)
    T[0,0]=Sx
    T[1,1]=Sy
    T[2,2]=Sz
    T[3,3]=1
    T[0,3]=avg[0]*(1-Sx)
    T[1,3]=avg[1]*(1-Sy)
    T[2,3]=avg[2]*(1-Sz)

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

def rotXAlongAxis(M, alpha):
    """Rotates polygon M around the polygon's own X axis by alpha degrees.
    This translates the polygon, rotates it and then translates it back.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    alpha_radians = np.radians(alpha)
    sin = np.sin(alpha_radians)
    cos = np.cos(alpha_radians)
    avg = np.average(M, axis=1)
    y = avg[1]
    z = avg[2]
    T[1,1] = cos
    T[2,2] = cos
    T[1,2] = -sin
    T[2,1] = sin
    T[1,3] = (y*(1-cos))+(z*sin)
    T[2,3] = (z*(1-cos))-(y*sin)
    return np.dot(T,M) 

def rotZAlongAxis(M, alpha):
    """Rotates polygon M around the polygon's own Z axis by alpha degrees.
    This translates the polygon, rotates it and then translates it back.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    alpha_radians = np.radians(alpha)
    sin = np.sin(alpha_radians)
    cos = np.cos(alpha_radians)
    avg = np.average(M, axis=1)
    x = avg[0]
    y = avg[1]
    T[0,0] = cos
    T[1,1] = cos
    T[0,1] = -sin
    T[1,0] = sin
    T[0,3] = (x*(1-cos))+(y*sin)
    T[1,3] = (y*(1-cos))-(x*sin)
    return np.dot(T,M) 

def rotYAlongAxis(M, alpha):
    """Rotates polygon M around the polygon's own Y axis by alpha degrees.
    This translates the polygon, rotates it and then translates it back.
    M needs to be a Numpy Array with shape (4,N) with N>=1"""
    T = np.eye(4)
    alpha_radians = np.radians(alpha)
    sin = np.sin(alpha_radians)
    cos = np.cos(alpha_radians)
    avg = np.average(M, axis=1)
    x = avg[0]
    z = avg[2]
    T[0,0] = cos
    T[2,2] = cos
    T[0,2] = sin
    T[2,0] = -sin
    T[0,3] = (x*(1-cos))-(z*sin)
    T[2,3] = (z*(1-cos))+(x*sin)
    return np.dot(T,M) 