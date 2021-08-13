from DataStructure.Matrices.transforms import translation
from DataStructure.DataStructure import Object
from DataStructure.Matrices.pipeline import first_pipeline, VRP_and_n, pipeline_steps
import numpy as np
from tkinter import *

#verificar de alterar as coordenadas da face dando o id pra ela, pra não ter que desenhar por cima depois e bugar o calculo do zbuffer que tinha sido feito
class Screen():
    def __init__(self, frame):
        self.objects = []
        self.number_objects = 0
        self.canvas = Canvas(frame, width = int(width*0.7), height = int(height*(0.9)), bg = "white")
        self.object_Selected = None

    def draw(self, object):
        self.objects[self.number_objects] = []
        for i in range(0, object.numberFaces):
            self.objects[self.number_objects].append(self.canvas.create_polygon(object.getCoordinates(i), outline='blue', fill='light blue', width = 2, tags = "objeto"))
        self.number_objects = self.number_objects + 1

    def selectFacesObject(self, face):
        for i in range(0, self.number_objects):
            if face in self.objects[i]:
                self.object_Selected = i
                return self.objects[i]



window = Tk()
window.title('The Marvelous Polygoneer')
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.state('zoomed')

frameDrawingInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.7), height = int(height*(0.9)))
frameDrawingInterface.place(x = int(width*0.01), y = int(height * 0.01))

UserInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.20), height = int(height*(0.9)))
UserInterface.place(x = int(width*0.75), y = int(height * 0.01))


#drawing = Canvas(frameDrawingInterface, width = int(width*0.7), height = int(height*(0.9)), bg = "white") 
drawing = Screen(frameDrawingInterface)

drawing.canvas.pack()



poliedro_teste = np.array([[30, 35, 25, 20,   30],
                           [ 2,  4,  3,  1,   10],
                           [25, 20, 18, 23, 22.5],
                           [ 1,  1,  1,  1,    1]])



def object_clicked(event):
    print("voce cricou no objeto")
    #drawing.canvas.delete("current")
    object = drawing.deleteObject(drawing.canvas.find_withtag("current")[0])
    for i in object:
        drawing.canvas.delete(i)


drawing.canvas.tag_bind("objeto", "<Button-1>", object_clicked)

def draw_objects(event):
    obj = Object(450, 150, 150, 150, 60, 100, 20)
    obj2 = Object(600, 600, 150, 150, 60, 100, 10)
    obj3 = Object(400, 400, 150, 150, 60, 100, 5)
    obj4 = Object(150, 150, 150, 150, 60, 100, 17)
    obj5 = Object(1, 1, 1, 200, 100, 100, 6)
    obj6 = Object(1000, 400, 250, 250, 60, 100, 18)


    drawing.draw(obj)
    drawing.draw(obj2)
    drawing.draw(obj3)
    drawing.draw(obj4)
    drawing.draw(obj5)
    drawing.draw(obj6)


def erase(event):
    if event.char == ' ':
        print("test")
        drawing.canvas.delete(ALL)

def select_object(event):
    if event.char == ' ':
        print("test")
    

drawing.canvas.bind_all('<space>', erase)
drawing.canvas.bind_all('<x>', draw_objects)
drawing.canvas.bind('<Button-1>', select_object)

window.mainloop()

value_move = 10


def move_object_x(value):
    x = 10
"""   
def move_object_y(value):
def move_object_z(value):
"""

#moveObject mandando o X, Y e Z -> translation
#scaleObject mandando o Sx, Sy, Sz -> escala
#rotObjectX mandando o value -> rotação
#rotObjectY mandando o value -> rotação
#rotObjectZ mandando o value -> rotation
translationValue = 5
scaleLessValue = 5
scaleMoreValue = 5
rotationValue = 5

def move_x_left():
    moveObject(-translationValue, 0, 0)

def move_x_right():
    moveObject(translationValue, 0, 0)

def move_z_front():
    moveObject(0, 0, translationValue)

def move_z_back():
    moveObject(0, 0, -translationValue)

def move_y_up():
    moveObject(0, translationValue, 0)

def move_y_down():
    moveObject(0, -translationValue, 0)

def scale_x_less():
    scaleObject(-scaleLessValue, 0, 0)

def scale_x_more():
    scaleObject(scaleMoreValue, 0, 0)

def scale_z_less():
    scaleObject(0, 0, -scaleLessValue)

def scale_z_more():
    scaleObject(0, 0, scaleMoreValue)

def scale_y_less():
    scaleObject(0, -scaleLessValue, 0)

def scale_y_more():
    scaleObject(0, scaleMoreValue, 0)

def rot_x_left():
    rotObjectX(-rotationValue)

def rot_x_right():
    rotObjectX(rotationValue)

def rot_z_front():
    rotObjectZ(rotationValue)

def rot_z_back():
    rotObjectZ(-rotationValue)

def rot_y_up():
    rotObjectY(rotationValue)

def rot_y_down():
    rotObjectY(-rotationValue)

drawing.canvas.bind_all('<q>', move_x_left)
drawing.canvas.bind_all('<a>', move_x_right)
drawing.canvas.bind_all('<w>', move_z_front)
drawing.canvas.bind_all('<s>', move_z_back)
drawing.canvas.bind_all('<e>', move_y_up)
drawing.canvas.bind_all('<d>', move_y_down)

drawing.canvas.bind_all('<r>', scale_x_less)
drawing.canvas.bind_all('<f>', scale_x_more)
drawing.canvas.bind_all('<t>', scale_z_less)
drawing.canvas.bind_all('<g>', scale_z_more)
drawing.canvas.bind_all('<y>', scale_y_less)
drawing.canvas.bind_all('<h>', scale_y_more)

drawing.canvas.bind_all('<u>', rot_x_left)
drawing.canvas.bind_all('<j>', rot_x_right)
drawing.canvas.bind_all('<i>', rot_z_front)
drawing.canvas.bind_all('<k>', rot_z_back)
drawing.canvas.bind_all('<o>', rot_y_up)
drawing.canvas.bind_all('<l>', rot_y_down)
