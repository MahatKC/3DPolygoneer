from Matrices.prism import create_prism
import numpy as np
import math

#counter clockwise
#fazer as funções para chamar os métodos do objeto
#quando clicar em um objeto, selecionar o objeto que esta sendo clicado
#fazer uma lista de objetos que estão existindo
#fazer um modo de ao clicar selecionar um dos objetos do tkinter
#fazer um modo de alterar esse objeto do tkinter e alterar na lista
#ver se consegue ao clicar pegar por exemplo a cor que esta o pixel na coordenada clicada, além de pegar a posição X e Y
class Object():
    def __init__(self, x, y, z, h, r_bottom, r_top, sides):
        self.vertex = create_prism(x, y, z, h, r_bottom, r_top, sides)
        self.faces = {}
        self.numberFaces = sides + 2
        self.sides = sides

        for i in range(0, sides): #ajeitar utilizando sem for
            self.faces[i] =  (i, (i + 1) % sides, ((i + 1) % sides) + sides , i + sides)
        self.faces[sides] = (np.arange(sides))
        self.faces[sides + 1] = (np.arange(sides) + sides)
        
        self.vertexFaces = {} 
        for i in range (0, sides * 2):  #ravel e unravel -> np.reshape(X, (4*len))[:2*len]
            self.vertexFaces[i] = (i % sides, (i + sides - 1) % sides, math.floor(i / sides) + sides)

    def getCoordinates(self, face):
        list = []
        for i in range(0, len(self.faces[face])):
            list.append(int(self.vertex[0][self.faces[face][i]]))
            list.append(int(self.vertex[1][self.faces[face][i]]))     
        return list