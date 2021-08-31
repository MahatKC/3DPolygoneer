import numpy as np

def sombreamento_constante(face_list, normals_list, VRP, ka, kd, ks, n, il, ila, fonte_luz):
    avg_list = [np.average(face, axis=1)[:3] for face in face_list]
    Ia = [ila[i]*ka[i]/255 for i in range(3)]
    color_list = [sombreamento_single_face(avg_list[face_idx], normals_list[face_idx], Ia, kd, ks, n, il, fonte_luz, VRP) for face_idx in range(len(face_list))]

    return color_list

def sombreamento_single_face(centroid, N, Ia, kd, ks, n, il, fonte_luz, VRP):
    L = fonte_luz-centroid
    L_normalized = L/(np.linalg.norm(L))
    N_dot_L = np.dot(N,L_normalized)
    has_diffuse = N_dot_L>0

    R = np.dot(2*N_dot_L,N)-L_normalized
    S = VRP-centroid
    S_normalized = S/(np.linalg.norm(S))
    R_dot_S = np.dot(R,S_normalized)
    has_specular = R_dot_S>0
    
    if has_specular:
        R_dot_S_pow_n = R_dot_S**n

    face_color = "#"

    for color in range(3):
        if has_diffuse:
            Id = il[color]*kd[color]*N_dot_L/255
        else:
            Id = 0
        if has_specular:
            Is = il[color]*ks[color]*R_dot_S_pow_n/255
        else:
            Is = 0

        It = Ia[color]+Id+Is    
        It /= 255
        It *= 4095
        if It> 4095:
            It = 4095
        It_int = int(np.round(It))

        if It_int < 16:
            face_color = face_color+"00"+hex(It_int)[2:]
        elif It_int < 256:
            face_color = face_color+"0"+hex(It_int)[2:]
        else:
            face_color += hex(It_int)[2:]            

    return face_color.upper()
