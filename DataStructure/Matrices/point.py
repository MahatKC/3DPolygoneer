import numpy as np

class p:
    """Creates an X, Y, Z coordinate array for a point p"""

    def __init__(self, x, y, z):
        self.p = np.array([x,y,z])

    def __str__(self):
        return str(self.p.tolist())
    
    def x(self):
        """Returns X"""
        return self.p[0]
    
    def y(self):
        """Returns Y"""
        return self.p[1]

    def z(self):
        """Returns Z"""
        return self.p[2]