import numpy as np

#parametros:
#lista_normais
#VRP

#OBJETO:
# ka  (r,g,b) ->kar, kag, kab -> ka = [kar, kag, kab] => ka
# kd  (r,g,b)                                         => kd
# ks  (r,g,b)                                         => ks
# n                                                   => n
#CENA:
# Il  (r,g,b)                                         => Il
# Ila (r,g,b)                                         => Ila
# x,y,z -> fonte_luz = np.array([x,y,z])              => fonte_luz

def sombreamento_constante(face_list, normals_list, VRP, ka, kd, ks, n, il, ila, fonte_luz):
    avg_list = [np.average(face, axis=1) for face in face_list]
    Ia = [ila[i]*ka[i] for i in range(3)]
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
            Id = il[color]*kd[color]*N_dot_L
        else:
            Id = 0
        if has_specular:
            Is = il[color]*ks[color]*R_dot_S_pow_n
        else:
            Is = 0

        It = Ia[color]+Id+Is

        if It>255:
            It = 255
        It_int = np.round(It)
        
        if It_int<16:
            face_color = face_color+"0"+hex(It_int)
        else:
            face_color += hex(It_int)

    return face_color.upper()
