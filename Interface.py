#from typing_extensions import IntVar
from tkscrolledframe import ScrolledFrame
import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, ttk
from tkinter.constants import ALL, E, N, NS, RIGHT, S, VERTICAL, W, Y 

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
    def __init__(self, master, janela, **kwargs):
        width = kwargs.pop('width', None)
        height = (kwargs.pop('height', None))
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)
        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        if(janela == 0):
            self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=250, height=155, bg=bg)
        if(janela == 1):
            self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=250, height=235, bg=bg)
        if(janela == 2):
            self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=250, height=200, bg=bg)
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

    def __init__(self, parent, text="", *args, **options):
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
            numberJanela = 0
        if(text == "Projeção"):
            numberJanela = 1
        if(text == "Iluminação e sombreamento"):
            numberJanela = 2
            
        #self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.sub_frame = VerticalScrolledFrame(self, borderwidth=1, janela=numberJanela, relief=tk.SUNKEN)

    def toggle(self):
        if bool(self.show.get()):
            #self.sub_frame.pack(fill="x", expand=1)
            self.sub_frame.pack(fill=tk.BOTH, expand=True) # fill window
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')

def lerRadioButton(_, __, ___):
    if(rbProjecao.get() == 1):
        txtPx['state'] = tk.DISABLED
        txtPy['state'] = tk.DISABLED
        txtPz['state'] = tk.DISABLED
    else:
        txtPx['state'] = tk.WRITABLE
        txtPy['state'] = tk.WRITABLE
        txtPz['state'] = tk.WRITABLE

if __name__ == "__main__":
    window = tk.Tk()
    window.title('The Marvelous Polygoneer')
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    
    #window.geometry("%dx%d+0+0" %(width, height))
    window.state('zoomed')

    # Fazendo Frame
    frameDrawingInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = int(width*0.7), height = int(height*(0.9)))
    frameDrawingInterface.place(x = int(width*0.01), y = int(height * 0.01))

    # Fazendo janela com as informações do usuário
    userInterface = Frame(window,  highlightbackground= "black", highlightthickness= 1, width = 280, height = 690)
    userInterface.place(x = int(width*0.75), y = int(height * 0.01))
    userInterface.pack_propagate(0)

    # Fazendo o canvas
    drawing = Canvas(frameDrawingInterface, width = int(width*0.7), height = int(height*(0.85)), bg = "white") 
    drawing.pack()

    btnLimpar = ttk.Button(window,text="Limpar", width=15)
    #btnLimpar.place(x=int(width*0.01), y = int(height * 0.88))
    btnLimpar.place(x=int(width*0.642), y = int(height * 0.88))

    # Salvando coortenadas
    drawing.old_coords = None

    drawing.bind("<ButtonPress-1>", draw_line)
    drawing.bind('<ButtonRelease-1>', draw_line)

    drawing.bind('<B1-Motion>', draw)
    drawing.bind('<ButtonRelease-1>', reset_coords)
    drawing.bind_all('<space>', erase)

    rbProjecao = tk.IntVar()
    rbProjecao.set(0)
    rbSombreamento = tk.IntVar()
    rbSombreamento.set(0)

    t = ToggledFrame(userInterface, text='Informações do objeto', relief="raised", borderwidth=1)
    t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    labelCg = ttk.Label(t.sub_frame, text='Centro geométrico')
    txtCg = ttk.Entry(t.sub_frame, name="txtCentroGeometrico", width=15)
    labelRaioBase = ttk.Label(t.sub_frame, text='Raio da base')
    txtRaioBase = ttk.Entry(t.sub_frame, name="txtRaioBase", width=15)
    labelRaioTopo = ttk.Label(t.sub_frame, text='Raio do topo')
    txtRaioTopo = ttk.Entry(t.sub_frame, name="txtRaioTopo", width=15)
    labelNumLados = ttk.Label(t.sub_frame, text='Número de lados')
    txtNumLados = ttk.Entry(t.sub_frame, name="txtNumLados", width=15)
    labelAltura = ttk.Label(t.sub_frame, text='Altura')
    txtAltura = ttk.Entry(t.sub_frame, name="txtAltura", width=15)
    btnAlterarObjeto = ttk.Button(t.sub_frame,text="Alterar objeto", width=15)

    labelCg.grid(row=1, column=1, padx=10, pady=1)
    txtCg.grid(row=1, column=2, padx=1, pady=1)
    labelRaioBase.grid(row=2, column=1, padx=1, pady=1)
    txtRaioBase.grid(row=2, column=2, padx=1, pady=1)
    labelRaioTopo.grid(row=3, column=1, padx=1, pady=1)
    txtRaioTopo.grid(row=3, column=2, padx=1, pady=1)
    labelNumLados.grid(row=4, column=1, padx=1, pady=1)
    txtNumLados.grid(row=4, column=2, padx=1, pady=1)
    labelAltura.grid(row=5, column=1, padx=1, pady=1)
    txtAltura.grid(row=5, column=2, padx=1, pady=1)
    btnAlterarObjeto.grid(row=6, column=1, padx=4, pady=8, columnspan=2)

    t2 = ToggledFrame(userInterface, text='Projeção', relief="raised", borderwidth=1)
    t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    labelTipoProjecao = ttk.Label(t2.sub_frame, text="Tipo de projeção", font="-weight bold -size 9")
    rbAxonometrica = ttk.Radiobutton(t2.sub_frame, text="Axonométrica", variable= rbProjecao, value=1)
    rbPerspectiva = ttk.Radiobutton(t2.sub_frame, text="Perspectiva", variable= rbProjecao, value=0)

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
    btnAlterarPlano = ttk.Button(t2.sub_frame,text="Alterar cena", width=15)

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
    btnAlterarPlano.grid(row=29, column=1, padx=4, pady=8, columnspan=2)

    rbProjecao.trace('w', lerRadioButton)

    t3 = ToggledFrame(userInterface, text='Iluminação e sombreamento', relief="raised", borderwidth=1)
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
    btnAlterarIluminacao = ttk.Button(t3.sub_frame,text="Alterar Ilum/Somb", width=20)

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

    window.mainloop()