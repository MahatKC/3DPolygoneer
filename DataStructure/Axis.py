from DataStructure.Matrices.pipeline import  pipeline_steps
from DataStructure.Matrices.transforms import translation
import numpy as np
class Axis():
    def __init__(self):
        self.size = 60
        self.axis = np.array([[0, self.size, 0, 0], [0, 0, self.size, 0], [0, 0, 0, self.size], [1, 1, 1, 1]])
        self.axisSRT = None
    
    def translation(self, valueX, valueY, valueZ):
        self.axis = translation(self.axis, valueX, valueY, valueZ)

    def pipeline_me(self, SRC_matrix, isPerspective, distanciaProjecao):
        self.axisSRT =  np.dot(SRC_matrix, self.axis)
        if isPerspective:
            proj = np.eye(4)
            proj[3, 2] = -1/distanciaProjecao
            self.axisSRT = np.dot(proj, self.axisSRT)
        self.axisSRT[1, :] *= -1