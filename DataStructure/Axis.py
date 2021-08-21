from DataStructure.Matrices.pipeline import  pipeline_steps
from DataStructure.Matrices.transforms import translation

class Axis():
    def __init__(self):
        self.size = 5
        self.axis = [[0, self.size, 0, 0], [0, 0, self.size, 0], [0, 0, 0, self.size], [1, 1, 1, 1]]
        self.axisSRT = None
    
    def translation(self, valueX, valueY, valueZ):
        self.axis = translation(self.axis, valueX, valueY, valueZ)

    def pipeline_me(self, SRC_matrix, jp_proj_matrix, dist_near, dist_far):
        _, self.axisSRT = pipeline_steps(self.axis, SRC_matrix, jp_proj_matrix, dist_near, dist_far)