#from typing_extensions import IntVar
from DataStructure.Matrices.transforms import translation
from shutil import disk_usage
from _pytest.store import D
from tkscrolledframe import ScrolledFrame
from Screen import Screen
import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, ttk
from tkinter.constants import ALL, E, N, NS, RIGHT, S, VERTICAL, W, Y 

"""def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))"""
class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so 
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, width, height, janela, **kwargs):
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)
        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT) 
        if(janela == 0):
            self.canvas = tk.Canvas(self.outer, highlightthickness=0, width = width, height = int(height * 0.13) , bg=bg)
        if(janela == 1):
            self.canvas = tk.Canvas(self.outer, highlightthickness=0, width = width, height = int(height * 0.41), bg=bg)
        if(janela == 2):
            self.canvas = tk.Canvas(self.outer, highlightthickness=0, width= width, height= int(height * 0.36), bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)
        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0, 0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)

numberJanela = 0
class ToggledFrame(tk.Frame):

    def __init__(self, parent, width, height, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1, padx=50)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        if(text == "Informações do objeto"):
            self.sub_frame = VerticalScrolledFrame(self, width, height, borderwidth=1, janela= 0, relief=tk.SUNKEN)
        if(text == "Projeção"):
            self.sub_frame = VerticalScrolledFrame(self, width, height, borderwidth=1, janela= 1, relief=tk.SUNKEN)
        if(text == "Iluminação e sombreamento"):
            self.sub_frame = VerticalScrolledFrame(self, width, height, borderwidth=1, janela= 2, relief=tk.SUNKEN)
        

        #self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        #self.sub_frame = VerticalScrolledFrame(self, width, height, borderwidth=1, janela=numberJanela, relief=tk.SUNKEN)

    def toggle(self):
        if bool(self.show.get()):
            #self.sub_frame.pack(fill="x", expand=1)
            self.sub_frame.pack(fill=tk.BOTH, expand=True) # fill window
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')

def lerRadioButton(_, __, ___):
    if(rbProjecao.get() == 0):
        txtPx['state'] = tk.DISABLED
        txtPy['state'] = tk.DISABLED
        txtPz['state'] = tk.DISABLED
    else:
        txtPx['state'] = tk.WRITABLE
        txtPy['state'] = tk.WRITABLE
        txtPz['state'] = tk.WRITABLE

def botaoObjeto(_, __, ___):
    if (drawing.objectSelected is not None):
        btnAlterarObjeto['state'] = tk.WRITABLE
        btnCriarObjeto['state'] = tk.DISABLED
    else:
        btnAlterarObjeto['state'] = tk.DISABLED
        btnCriarObjeto['state'] = tk.WRITABLE

def ClearScreen():
    drawing.ClearAll()

def SendUI(values): # PEGAR VALORES DO PIPELINE E ATUALIZAR NAS INFORMAÇÕES DO OBJETO
    print(values)
    txtNumLados.delete(0, tk.END)
    txtNumLados.insert(0, str(values[0]))
    txtRaioBase.delete(0, tk.END)
    txtRaioBase.insert(0, str(values[1]))
    txtRaioTopo.delete(0, tk.END)
    txtRaioTopo.insert(0, str(values[2]))
    txtAltura.delete(0, tk.END)
    txtAltura.insert(0, str(values[3]))

translationValue = 5
scaleLessValue = 0.9
scaleMoreValue = 1.111111
rotationValue = 5

def move_x_left(event):
    drawing.moveObject(-translationValue, 0, 0)
    SendUI(drawing.GetAttributes())

def move_x_right(event):
    drawing.moveObject(translationValue, 0, 0)
    SendUI(drawing.GetAttributes())

def move_z_front(event):
    drawing.moveObject(0, 0, translationValue)
    SendUI(drawing.GetAttributes())

def move_z_back(event):
    drawing.moveObject(0, 0, -translationValue)
    SendUI(drawing.GetAttributes())

def move_y_up(event):
    drawing.moveObject(0, translationValue, 0)
    SendUI(drawing.GetAttributes())

def move_y_down(event):
    drawing.moveObject(0, -translationValue, 0)
    SendUI(drawing.GetAttributes())

def scale_x_less(event):
    drawing.scaleObject(scaleLessValue, 1, 1)
    SendUI(drawing.GetAttributes())

def scale_x_more(event):
    drawing.scaleObject(scaleMoreValue, 1, 1)
    SendUI(drawing.GetAttributes())

def scale_z_less(event):
    drawing.scaleObject(1, 1, scaleLessValue)
    SendUI(drawing.GetAttributes())

def scale_z_more(event):
    drawing.scaleObject(1, 1, scaleMoreValue)
    SendUI(drawing.GetAttributes())

def scale_y_less(event):
    drawing.scaleObject(1, scaleLessValue, 1)
    SendUI(drawing.GetAttributes())

def scale_y_more(event):
    drawing.scaleObject(1, scaleMoreValue, 1)
    SendUI(drawing.GetAttributes())

def rot_x_left(event):
    drawing.rotObjectX(-rotationValue)
    SendUI(drawing.GetAttributes())

def rot_x_right(event):
    drawing.rotObjectX(rotationValue)
    SendUI(drawing.GetAttributes())

def rot_z_front(event):
    drawing.rotObjectZ(rotationValue)
    SendUI(drawing.GetAttributes())

def rot_z_back(event):
    drawing.rotObjectZ(-rotationValue)
    SendUI(drawing.GetAttributes())

def rot_y_up(event):
    drawing.rotObjectY(rotationValue)
    SendUI(drawing.GetAttributes())

def rot_y_down(event):
    drawing.rotObjectY(-rotationValue)
    SendUI(drawing.GetAttributes())

def SelectingObject(event):
    if event.widget.find_withtag("current"):
        object = drawing.ObjectSelection(drawing.canvas.find_withtag("current")[0])
        SendUI(drawing.GetAttributes())
        for i in object:
            drawing.canvas.itemconfig(i, fill='red')
            #drawing.canvas.coords(i, [30, 30, 50, 80, 100, 100, 200, 200, 420, 100]) #readapta as coordenadas de cada face do objeto
    else:
        drawing.objectSelected = None
    botaoObjeto(1, 2, 3)
    
def atualizarObjeto():
    numLados = int(isVazio(txtNumLados.get()))
    altura = isVazio(txtAltura.get())
    raioBase = isVazio(txtRaioBase.get())
    raioTopo = isVazio(txtRaioTopo.get()) 

    drawing.UpdateObject(raioBase, raioTopo, numLados, altura)

def objetoClick():
    numLados = int(isVazio(txtNumLados.get()))
    altura = isVazio(txtAltura.get())
    raioBase = isVazio(txtRaioBase.get())
    raioTopo = isVazio(txtRaioTopo.get())

    drawing.AddObjects(raioBase, raioTopo, numLados, altura)

def criarObjeto(numLados, altura, raioBase, raioTopo):
    print(numLados*4)

def projecaoSet(values):
    txtVRPx.delete(0, tk.END)
    txtVRPx.insert(0, str(values[0]))
    txtVRPy.delete(0, tk.END)
    txtVRPy.insert(0, str(values[1]))
    txtVRPz.delete(0, tk.END)
    txtVRPz.insert(0, str(values[2]))
    txtPx.delete(0, tk.END)
    txtPx.insert(0, str(values[3]))
    txtPy.delete(0, tk.END)
    txtPy.insert(0, str(values[4]))
    txtPz.delete(0, tk.END)
    txtPz.insert(0, str(values[5]))
    txtViewUpx.delete(0, tk.END)
    txtViewUpx.insert(0, str(values[6]))
    txtViewUpy.delete(0, tk.END)
    txtViewUpy.insert(0, str(values[7]))
    txtViewUpz.delete(0, tk.END)
    txtViewUpz.insert(0, str(values[8]))
    txtNear.delete(0, tk.END)
    txtNear.insert(0, str(values[9]))
    txtFar.delete(0, tk.END)
    txtFar.insert(0, str(values[10]))
    txtPlanoProjecao.delete(0, tk.END)
    txtPlanoProjecao.insert(0, str(values[11]))
    txtLimMundoxMin.delete(0, tk.END)
    txtLimMundoxMin.insert(0, str(values[12]))
    txtLimMundoxMax.delete(0, tk.END)
    txtLimMundoxMax.insert(0, str(values[13]))
    txtLimMundoyMin.delete(0, tk.END)
    txtLimMundoyMin.insert(0, str(values[14]))
    txtLimMundoyMax.delete(0, tk.END)
    txtLimMundoyMax.insert(0, str(values[15]))
    txtLimPlanoProjxMin.delete(0, tk.END)
    txtLimPlanoProjxMin.insert(0, str(values[16]))
    txtLimPlanoProjxMax.delete(0, tk.END)
    txtLimPlanoProjxMax.insert(0, str(values[17]))
    txtLimPlanoProjyMin.delete(0, tk.END)
    txtLimPlanoProjyMin.insert(0, str(values[18]))
    txtLimPlanoProjyMax.delete(0, tk.END)
    txtLimPlanoProjyMax.insert(0, str(values[19]))


def projecaoClick():
    #rbProjeção = 0 -> perspectiva; rbProjeção = 1 -> axonometrica
    projecao = bool(int(rbProjecao.get())) # mudar pra true ou false
    vrpX = isVazio(txtVRPx.get())
    vrpY = isVazio(txtVRPy.get())
    vrpZ = isVazio(txtVRPz.get())
    pX = isVazio(txtPx.get())
    pY = isVazio(txtPy.get())
    pZ = isVazio(txtPz.get())
    viewUpX = isVazio(txtViewUpx.get())
    viewUpY = isVazio(txtViewUpy.get())
    viewUpZ = isVazio(txtViewUpz.get())
    near = isVazio(txtNear.get())
    far = isVazio(txtFar.get())
    planoProj = isVazio(txtPlanoProjecao.get())
    mundoxMin = isVazio(txtLimMundoxMin.get())
    mundoxMax = isVazio(txtLimMundoxMax.get())
    mundoyMin = isVazio(txtLimMundoyMin.get())
    mundoyMax = isVazio(txtLimMundoyMax.get())
    planoProjxMin = isVazio(txtLimPlanoProjxMin.get())
    planoProjxMax = isVazio(txtLimPlanoProjxMax.get())
    planoProjyMin = isVazio(txtLimPlanoProjyMin.get())
    planoProjyMax = isVazio(txtLimPlanoProjyMax.get())

    drawing.RedoPipeline(projecao, vrpX, vrpY, vrpZ, pX, pY, pZ, viewUpX, viewUpY, viewUpZ, near, far, planoProj,
                mundoxMin, mundoxMax, mundoyMin, mundoyMax, planoProjxMin, planoProjxMax, planoProjyMin, planoProjyMax)
                
    projecaoSet(drawing.GetProjecao())

def iluminacaoClick():
    #sombreamento = 0 -> constante; sombreamento = 1 -> gourad; sombreamento = 2 -> phong
    sombreamento = int(rbSombreamento.get())
    ka = isVazio(txtKa.get())
    kd = isVazio(txtKd.get())
    ks = isVazio(txtKs.get())
    n = isVazio(txtN.get())
    criarIluminacao(sombreamento, ka, kd, ks, n)

def isVazio(string):
    if(string == ""):
        return 0.0
    return float(string)

def criarIluminacao(sombreamento, ka, kd, ks, n):
    print(sombreamento*2)

if __name__ == "__main__":
    window = tk.Tk()
    window.title('The Marvelous Polygoneer')
    width = window.winfo_screenwidth()  
    height = window.winfo_screenheight()
    window.state('zoomed')
    # Fazendo Frame
    frameDrawingInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.7), height = int(height*0.88))
    frameDrawingInterface.place(x = int(width*0.01), y = int(height * 0.01)) 

    # Fazendo janela com as informações do usuário
    userInterface = Frame(window, highlightbackground= "black", highlightthickness= 1, width = int(width*0.27), height = int(height*0.88))
    userInterface.place(x = int(width*0.72), y = int(height * 0.01))
    userInterface.pack_propagate(0)

    # Fazendo o canvas
    drawing = Screen(frameDrawingInterface, width, height) 
    drawing.canvas.pack()

    btnLimpar = ttk.Button(window,text="Limpar", width=15, command = ClearScreen) 
    #btnLimpar.place(x=int(width*0.01), y = int(height * 0.88))
    btnLimpar.place(x=int(width*0.66), y = int(height * 0.9))

    drawing.canvas.bind('<Button-1>', SelectingObject)

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

    rbProjecao = tk.IntVar()
    rbProjecao.set(0)
    rbSombreamento = tk.IntVar()
    rbSombreamento.set(0)
    textNumLados = tk.StringVar()
    textNumLados.set("")

    t = ToggledFrame(userInterface, width, height, text='Informações do objeto', relief="raised", borderwidth=1)
    t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    labelRaioBase = ttk.Label(t.sub_frame, text='Raio da base')
    txtRaioBase = ttk.Entry(t.sub_frame, name="txtRaioBase", width=15)
    labelRaioTopo = ttk.Label(t.sub_frame, text='Raio do topo')
    txtRaioTopo = ttk.Entry(t.sub_frame, name="txtRaioTopo", width=15)
    labelNumLados = ttk.Label(t.sub_frame, text='Número de lados')
    txtNumLados = ttk.Entry(t.sub_frame, name="txtNumLados", width=15, textvariable=textNumLados)
    labelAltura = ttk.Label(t.sub_frame, text='Altura')
    txtAltura = ttk.Entry(t.sub_frame, name="txtAltura", width=15)
    btnCriarObjeto = ttk.Button(t.sub_frame,text="Criar objeto", width=15, command=objetoClick)
    btnAlterarObjeto = ttk.Button(t.sub_frame,text="Alterar objeto", width=15, command=atualizarObjeto)

    labelNumLados.grid(row=1, column=1, padx=10, pady=1)
    txtNumLados.grid(row=1, column=2, padx=1, pady=1)
    labelRaioBase.grid(row=2, column=1, padx=1, pady=1)
    txtRaioBase.grid(row=2, column=2, padx=1, pady=1)
    labelRaioTopo.grid(row=3, column=1, padx=1, pady=1)
    txtRaioTopo.grid(row=3, column=2, padx=1, pady=1)
    labelAltura.grid(row=5, column=1, padx=1, pady=1)
    txtAltura.grid(row=5, column=2, padx=1, pady=1)
    btnCriarObjeto.grid(row=6, column=1, padx=4, pady=8)
    btnAlterarObjeto.grid(row=6, column=2, padx=4, pady=8)

    textNumLados.trace('w', botaoObjeto)
    t2 = ToggledFrame(userInterface, width, height, text='Projeção', relief="raised", borderwidth=1)
    t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    labelTipoProjecao = ttk.Label(t2.sub_frame, text="Tipo de projeção", font="-weight bold -size 9")
    rbAxonometrica = ttk.Radiobutton(t2.sub_frame, text="Axonométrica", variable= rbProjecao, value=0)
    rbPerspectiva = ttk.Radiobutton(t2.sub_frame, text="Perspectiva", variable= rbProjecao, value=1)

    labelVRP = ttk.Label(t2.sub_frame, text="VRP", font="-weight bold -size 9")
    labelVRPx = ttk.Label(t2.sub_frame, text="X")
    txtVRPx = ttk.Entry(t2.sub_frame, name="txtVRPx", width=15)
    labelVRPy = ttk.Label(t2.sub_frame, text="Y")
    txtVRPy= ttk.Entry(t2.sub_frame, name="txtVRPy", width=15)
    labelVRPz = ttk.Label(t2.sub_frame, text="Z")
    txtVRPz = ttk.Entry(t2.sub_frame, name="txtVRPz", width=15)

    labelP = ttk.Label(t2.sub_frame, text="Vetor P", font="-weight bold -size 9")
    labelPx = ttk.Label(t2.sub_frame, text="X")
    txtPx = ttk.Entry(t2.sub_frame, name="txtPx", width=15)
    labelPy = ttk.Label(t2.sub_frame, text="Y")
    txtPy= ttk.Entry(t2.sub_frame, name="txtPy", width=15)
    labelPz = ttk.Label(t2.sub_frame, text="Z")
    txtPz = ttk.Entry(t2.sub_frame, name="txtPz", width=15)

    labelViewUp = ttk.Label(t2.sub_frame, text="Vetor View-up", font="-weight bold -size 9")
    labelViewUpx = ttk.Label(t2.sub_frame, text="X")
    txtViewUpx = ttk.Entry(t2.sub_frame, name="txtViewUpx", width=15)
    labelViewUpy = ttk.Label(t2.sub_frame, text="Y")
    txtViewUpy= ttk.Entry(t2.sub_frame, name="txtViewUpy", width=15)
    labelViewUpz = ttk.Label(t2.sub_frame, text="Z")
    txtViewUpz = ttk.Entry(t2.sub_frame, name="txtViewUpz", width=15)

    labelDistancia = ttk.Label(t2.sub_frame, text="Distâncias", font="-weight bold -size 9")
    labelNear = ttk.Label(t2.sub_frame, text="Plano Near")
    txtNear = ttk.Entry(t2.sub_frame, name="txtNear", width=15)
    labelFar = ttk.Label(t2.sub_frame, text="Plano Far")
    txtFar= ttk.Entry(t2.sub_frame, name="txtFar", width=15)
    labelPlanoProjecao = ttk.Label(t2.sub_frame, text="Plano de projeção")
    txtPlanoProjecao = ttk.Entry(t2.sub_frame, name="txtPlanoProjecao", width=15)

    labelLimMundo = ttk.Label(t2.sub_frame, text="Limites do mundo", font="-weight bold -size 9")
    labelLimMundoxMin = ttk.Label(t2.sub_frame, text="X min")
    txtLimMundoxMin = ttk.Entry(t2.sub_frame, name="txtLimMundoxMin", width=15)
    labelLimMundoxMax = ttk.Label(t2.sub_frame, text="X max")
    txtLimMundoxMax = ttk.Entry(t2.sub_frame, name="txtLimMundoxMax", width=15)
    labelLimMundoyMin = ttk.Label(t2.sub_frame, text="Y min")
    txtLimMundoyMin = ttk.Entry(t2.sub_frame, name="txtLimMundoyMin", width=15)
    labelLimMundoyMax = ttk.Label(t2.sub_frame, text="Y max")
    txtLimMundoyMax = ttk.Entry(t2.sub_frame, name="txtLimMundoyMax", width=15)

    labelLimPlanoProj = ttk.Label(t2.sub_frame, text="Plano de projeção", font="-weight bold -size 9")
    labelLimPlanoProjxMin = ttk.Label(t2.sub_frame, text="X min")
    txtLimPlanoProjxMin = ttk.Entry(t2.sub_frame, name="txtLimPlanoProjxMin", width=15)
    labelLimPlanoProjxMax = ttk.Label(t2.sub_frame, text="X max")
    txtLimPlanoProjxMax = ttk.Entry(t2.sub_frame, name="txtLimPlanoProjxMax", width=15)
    labelLimPlanoProjyMin = ttk.Label(t2.sub_frame, text="Y min")
    txtLimPlanoProjyMin = ttk.Entry(t2.sub_frame, name="txtLimPlanoProjyMin", width=15)
    labelLimPlanoProjyMax = ttk.Label(t2.sub_frame, text="Y max")
    txtLimPlanoProjyMax = ttk.Entry(t2.sub_frame, name="txtLimPlanoProjyMax", width=15)
    btnAlterarCena = ttk.Button(t2.sub_frame,text="Alterar cena", width=15, command=projecaoClick)

    labelTipoProjecao.grid(row=1, column=1, padx=1, pady=2)
    rbAxonometrica.grid(row=2, column=1, padx=5, pady=2)
    rbPerspectiva.grid(row=2, column=2, padx=5, pady=2) 
    
    labelVRP.grid(row=3, column=1, padx=10, pady=2, sticky=W)
    labelVRPx.grid(row=4, column=1, padx=1, pady=1)
    txtVRPx.grid(row=4, column=2, padx=1, pady=1)
    labelVRPy.grid(row=5, column=1, padx=1, pady=1)
    txtVRPy.grid(row=5, column=2, padx=1, pady=1)
    labelVRPz.grid(row=6, column=1, padx=1, pady=1)
    txtVRPz.grid(row=6, column=2, padx=1, pady=1)

    labelP.grid(row=7, column=1, padx=10, pady=2, sticky=W)
    labelPx.grid(row=8, column=1, padx=1, pady=1)
    txtPx.grid(row=8, column=2, padx=1, pady=1)
    labelPy.grid(row=9, column=1, padx=1, pady=1)
    txtPy.grid(row=9, column=2, padx=1, pady=1)
    labelPz.grid(row=10, column=1, padx=1, pady=1)
    txtPz.grid(row=10, column=2, padx=1, pady=1)

    labelViewUp.grid(row=11, column=1, padx=10, pady=2, sticky=W)
    labelViewUpx.grid(row=12, column=1, padx=1, pady=1)
    txtViewUpx.grid(row=12, column=2, padx=1, pady=1)
    labelViewUpy.grid(row=13, column=1, padx=1, pady=1)
    txtViewUpy.grid(row=13, column=2, padx=1, pady=1)
    labelViewUpz.grid(row=14, column=1, padx=1, pady=1)
    txtViewUpz.grid(row=14, column=2, padx=1, pady=1)

    labelDistancia.grid(row=15, column=1, padx=10, pady=2, sticky=W)
    labelNear.grid(row=16, column=1, padx=1, pady=1)
    txtNear.grid(row=16, column=2, padx=1, pady=1)
    labelFar.grid(row=17, column=1, padx=1, pady=1)
    txtFar.grid(row=17, column=2, padx=1, pady=1)
    labelPlanoProjecao.grid(row=18, column=1, padx=1, pady=1)
    txtPlanoProjecao.grid(row=18, column=2, padx=1, pady=1)

    labelLimMundo.grid(row=19, column=1, padx=10, pady=4, sticky=W)
    labelLimMundoxMin.grid(row=20, column=1, padx=1, pady=1)
    txtLimMundoxMin.grid(row=20, column=2, padx=1, pady=1)
    labelLimMundoxMax.grid(row=21, column=1, padx=1, pady=1)
    txtLimMundoxMax.grid(row=21, column=2, padx=1, pady=1)
    labelLimMundoyMin.grid(row=22, column=1, padx=1, pady=1)
    txtLimMundoyMin.grid(row=22, column=2, padx=1, pady=1)
    labelLimMundoyMax.grid(row=23, column=1, padx=1, pady=1)
    txtLimMundoyMax.grid(row=23, column=2, padx=1, pady=1)

    labelLimPlanoProj.grid(row=24, column=1, padx=10, pady=4, sticky=W)
    labelLimPlanoProjxMin.grid(row=25, column=1, padx=1, pady=1)
    txtLimPlanoProjxMin.grid(row=25, column=2, padx=1, pady=1)
    labelLimPlanoProjxMax.grid(row=26, column=1, padx=1, pady=1)
    txtLimPlanoProjxMax.grid(row=26, column=2, padx=1, pady=1)
    labelLimPlanoProjyMin.grid(row=27, column=1, padx=1, pady=1)
    txtLimPlanoProjyMin.grid(row=27, column=2, padx=1, pady=1)
    labelLimPlanoProjyMax.grid(row=28, column=1, padx=1, pady=1)
    txtLimPlanoProjyMax.grid(row=28, column=2, padx=1, pady=1)
    btnAlterarCena.grid(row=29, column=1, padx=4, pady=8, columnspan=2)

    rbProjecao.trace('w', lerRadioButton)

    t3 = ToggledFrame(userInterface, width, height, text='Iluminação e sombreamento', relief="raised", borderwidth=1)
    t3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    labelIluminacao = ttk.Label(t3.sub_frame, text="Iluminação", font="-weight bold -size 9")
    labelKa = ttk.Label(t3.sub_frame, text='Ka')
    txtKa = ttk.Entry(t3.sub_frame, name="ka", width=15)
    labelKd = ttk.Label(t3.sub_frame, text='Kd')
    txtKd = ttk.Entry(t3.sub_frame, name="kd", width=15)
    labelKs = ttk.Label(t3.sub_frame, text='Ks')
    txtKs = ttk.Entry(t3.sub_frame, name="ks", width=15)
    labelN = ttk.Label(t3.sub_frame, text='n')
    txtN = ttk.Entry(t3.sub_frame, name="n", width=15)

    labelTipoSombreamento = ttk.Label(t3.sub_frame, text="Sombreamento", font="-weight bold -size 9")
    rbConstante = ttk.Radiobutton(t3.sub_frame, text="Constante", variable= rbSombreamento, value=0)
    rbGourad = ttk.Radiobutton(t3.sub_frame, text="Gourad", variable= rbSombreamento, value=1)
    rbPhong = ttk.Radiobutton(t3.sub_frame, text="Phong", variable= rbSombreamento, value=2)
    btnAlterarIluminacao = ttk.Button(t3.sub_frame,text="Alterar Ilum/Somb", width=20, command=iluminacaoClick)

    labelTipoSombreamento.grid(row=1, column=1, padx=12, pady=4, sticky=W)
    rbConstante.grid(row=2, column=1, padx=25, pady=1, sticky=W)
    rbGourad.grid(row=3, column=1, padx=25, pady=1, sticky=W)
    rbPhong.grid(row=4, column=1, padx=25, pady=1, sticky=W)

    labelIluminacao.grid(row=5, column=1, padx=12, pady=4, sticky=W)
    labelKa.grid(row=6, column=1, padx=1, pady=1)
    txtKa.grid(row=6, column=2, padx=1, pady=1)
    labelKd.grid(row=7, column=1, padx=1, pady=1)
    txtKd.grid(row=7, column=2, padx=1, pady=1)
    labelKs.grid(row=8, column=1, padx=1, pady=1)
    txtKs.grid(row=8, column=2, padx=1, pady=1)
    labelN.grid(row=9, column=1, padx=1, pady=1)
    txtN.grid(row=9, column=2, padx=1, pady=1)

    btnAlterarIluminacao.grid(row=10, column=1, padx=4, pady=8, columnspan=2)

    botaoObjeto(1, 1, 1)
    projecaoSet(drawing.GetProjecao())

    #window.bind('<Motion>', motion)
    window.mainloop()