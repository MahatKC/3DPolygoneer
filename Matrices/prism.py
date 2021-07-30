import numpy as np

def vertices(sides, radius, center, is_top):
    """Returns a NumPy matrix for a polygon in 3D space with homogeneous coordinates.
    The polygon is created based on the given number of sides, being circunscribed
    by a circle defined by the given parameters."""
    if is_top:
        vertices = (np.zeros((2,sides))+np.arange(sides))*np.radians(360/sides)
    else:
        vertices = (np.zeros((2,sides))+np.arange(sides)[::-1])*np.radians(360/sides)
    vertices[0,:] = np.cos(vertices[0,:])
    vertices[1,:] = np.sin(vertices[1,:])
    return np.concatenate((np.concatenate((vertices,np.zeros((1,sides))),axis=0)*radius + center,np.ones((1,sides))),axis=0)

def create_prism(x,y,z,h,r_bottom,r_top,sides):
    """Uses the coordinates of the center of the bottom circle.
    Returns a NumPy array for a 3D-prism with homogeneous coordinates.
    The first "sides" vertices define the polygon at the bottom of it,
    while the next "sides" vertices define the polygon on top of it.
    The last vertix is actually the geometric center of the object, stored for ease of use."""
    return np.concatenate((vertices(sides, r_top, np.array([[x],[y],[z+h]]),True),vertices(sides, r_bottom, np.array([[x],[y],[z]]),False)),axis=1)
