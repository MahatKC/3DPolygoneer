import numpy as np

def normal_test(faces, n):    
    v1 = faces[1]
    face_normal = np.cross(faces[2]-v1, faces[0]-v1)
    N_normalized = face_normal/(np.linalg.norm(face_normal))
    
    return (np.dot(N_normalized,n) > 0),N_normalized