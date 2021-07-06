import numpy as np
np.set_printoptions(suppress=True, precision=6)
import time

class prism():
    def __init__(self,x,y,z,h,r1,r2,sides):
        """Defines a prism based on two circles. 
        First circle has coordinates x,y,z and radius r1.
        Second circle has has same coordinates x and y from first circle,
        but its third coordinate is z+h, h being the prism's height.
        The second circle's radius is r2.
        The prism has two polygons with the same number of sides as its bases.
        Both bases are circunscribed by their respective circles."""

        self.center_bottom = np.array([x,y,z])
        self.height = h
        self.r_bottom = r1
        self.r_top = r2
        self.center_top = np.array([x,y,z+h])
        self.sides = sides

def vertices(sides, radius, center_bottom):
    vertices = (np.zeros((2,sides))+np.arange(sides))*np.radians(360/sides)
    vertices[0,:] = np.cos(vertices[0,:])
    vertices[1,:] = np.sin(vertices[1,:])
    vertices = np.concatenate((vertices,np.zeros((1,np.shape(vertices)[1]))),axis=0)*radius + np.reshape(center_bottom, (1,np.shape(center_bottom)[0])).T
    
    return vertices

F = prism(1,2,3,4,5,6,20)
upper_vertices = vertices(F.sides, F.r_bottom, F.center_bottom)
bottom_vertices = vertices(F.sides, F.r_top, F.center_top)


