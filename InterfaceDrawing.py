from tkinter import *

def draw(event):
    x, y = event.x, event.y
    if drawing.old_coords:
        x1, y1 = drawing.old_coords
        drawing.create_line(x, y, x1, y1)
    drawing.old_coords = x, y

def draw_line(event):

    if str(event.type) == 'ButtonPress':
        drawing.old_coords = event.x, event.y

    elif str(event.type) == 'ButtonRelease':
        x, y = event.x, event.y
        x1, y1 = drawing.old_coords
        drawing.create_line(x, y, x1, y1)

def reset_coords(event):
    drawing.old_coords = None



def erase(event):
    if event.char == ' ':
        print("test")
        drawing.delete(ALL)

window = Tk()
window.title('The Marvelous Polygoneer')
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
#window.geometry("%dx%d+0+0" %(width, height))
window.state('zoomed')

# Fazendo Frame
frameDrawingInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.7), height = int(height*(0.9)))
frameDrawingInterface.place(x = int(width*0.01), y = int(height * 0.01))

UserInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.20), height = int(height*(0.9)))
UserInterface.place(x = int(width*0.75), y = int(height * 0.01))


# Fazendo o canvas
drawing = Canvas(frameDrawingInterface, width = int(width*0.7), height = int(height*(0.9)), bg = "white") 
drawing.pack()

# Salvando coortenadas
drawing.old_coords = None


drawing.bind("<ButtonPress-1>", draw_line)
drawing.bind('<ButtonRelease-1>', draw_line)

drawing.bind('<B1-Motion>', draw)
drawing.bind('<ButtonRelease-1>', reset_coords)
drawing.bind_all('<space>', erase)

window.mainloop()