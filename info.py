#from typing_extensions import IntVar
from tkscrolledframe import ScrolledFrame
import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, ttk
from tkinter.constants import N, NS, RIGHT, S, VERTICAL, W, Y 

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
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = (kwargs.pop('height', None))
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
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
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

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

class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        #self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)
        self.sub_frame = VerticalScrolledFrame(self, 
        borderwidth=1, 
        relief=tk.SUNKEN)

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

    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(str(int(width*0.2))+"x"+str(height))
    rbProjecao = tk.IntVar()
    rbProjecao.set(0)

    t = ToggledFrame(root, text='Informações do objeto', relief="raised", borderwidth=1)
    t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    labelCg = ttk.Label(t.sub_frame, text='Centro geométrico')
    txtCg = ttk.Entry(t.sub_frame, name="txtCentroGeometrico")
    labelRaioBase = ttk.Label(t.sub_frame, text='Raio da base')
    txtRaioBase = ttk.Entry(t.sub_frame, name="txtRaioBase")
    labelRaioTopo = ttk.Label(t.sub_frame, text='Raio do topo')
    txtRaioTopo = ttk.Entry(t.sub_frame, name="txtRaioTopo")
    labelNumLados = ttk.Label(t.sub_frame, text='Número de lados')
    txtNumLados = ttk.Entry(t.sub_frame, name="txtNumLados")
    labelAltura = ttk.Label(t.sub_frame, text='Altura')
    txtAltura = ttk.Entry(t.sub_frame, name="txtAltura")

    labelCg.grid(row=1, column=1, padx=1, pady=1)
    txtCg.grid(row=1, column=2, padx=1, pady=1)
    labelRaioBase.grid(row=2, column=1, padx=1, pady=1)
    txtRaioBase.grid(row=2, column=2, padx=1, pady=1)
    labelRaioTopo.grid(row=3, column=1, padx=1, pady=1)
    txtRaioTopo.grid(row=3, column=2, padx=1, pady=1)
    labelNumLados.grid(row=4, column=1, padx=1, pady=1)
    txtNumLados.grid(row=4, column=2, padx=1, pady=1)
    labelAltura.grid(row=5, column=1, padx=1, pady=1)
    txtAltura.grid(row=5, column=2, padx=1, pady=1)

    t2 = ToggledFrame(root, text='Projeção', relief="raised", borderwidth=1)
    t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    labelTipoProjecao = ttk.Label(t2.sub_frame, text="Tipo de projeção", font="-weight bold -size 9")
    rbAxonometrica = ttk.Radiobutton(t2.sub_frame, text="Axonométrica", variable= rbProjecao, value=1)
    rbPerspectiva = ttk.Radiobutton(t2.sub_frame, text="Perspectiva", variable= rbProjecao, value=0)

    labelVRP = ttk.Label(t2.sub_frame, text="VRP", font="-weight bold -size 9")
    labelVRPx = ttk.Label(t2.sub_frame, text="X")
    txtVRPx = ttk.Entry(t2.sub_frame, name="txtVRPx")
    labelVRPy = ttk.Label(t2.sub_frame, text="Y")
    txtVRPy= ttk.Entry(t2.sub_frame, name="txtVRPy")
    labelVRPz = ttk.Label(t2.sub_frame, text="Z")
    txtVRPz = ttk.Entry(t2.sub_frame, name="txtVRPz")

    labelP = ttk.Label(t2.sub_frame, text="Vetor P", font="-weight bold -size 9")
    labelPx = ttk.Label(t2.sub_frame, text="X")
    txtPx = ttk.Entry(t2.sub_frame, name="txtPx")
    labelPy = ttk.Label(t2.sub_frame, text="Y")
    txtPy= ttk.Entry(t2.sub_frame, name="txtPy")
    labelPz = ttk.Label(t2.sub_frame, text="Z")
    txtPz = ttk.Entry(t2.sub_frame, name="txtPz")

    labelViewUp = ttk.Label(t2.sub_frame, text="Vetor View-up", font="-weight bold -size 9")
    labelViewUpx = ttk.Label(t2.sub_frame, text="X")
    txtViewUpx = ttk.Entry(t2.sub_frame, name="txtViewUpx")
    labelViewUpy = ttk.Label(t2.sub_frame, text="Y")
    txtViewUpy= ttk.Entry(t2.sub_frame, name="txtViewUpy")
    labelViewUpz = ttk.Label(t2.sub_frame, text="Z")
    txtViewUpz = ttk.Entry(t2.sub_frame, name="txtViewUpz")

    labelDistancia = ttk.Label(t2.sub_frame, text="Distâncias", font="-weight bold -size 9")
    labelNear = ttk.Label(t2.sub_frame, text="Plano Near")
    txtNear = ttk.Entry(t2.sub_frame, name="txtNear")
    labelFar = ttk.Label(t2.sub_frame, text="Plano Far")
    txtFar= ttk.Entry(t2.sub_frame, name="txtFar")
    labelPlanoProjecao = ttk.Label(t2.sub_frame, text="Plano de projeção")
    txtPlanoProjecao = ttk.Entry(t2.sub_frame, name="txtPlanoProjecao")

    labelLimMundo = ttk.Label(t2.sub_frame, text="Limites do mundo", font="-weight bold -size 9")
    labelLimMundoxMin = ttk.Label(t2.sub_frame, text="X min")
    txtLimMundoxMin = ttk.Entry(t2.sub_frame, name="txtLimMundoxMin")
    labelLimMundoxMax = ttk.Label(t2.sub_frame, text="X max")
    txtLimMundoxMax = ttk.Entry(t2.sub_frame, name="txtLimMundoxMax")
    labelLimMundoyMin = ttk.Label(t2.sub_frame, text="Y min")
    txtLimMundoyMin = ttk.Entry(t2.sub_frame, name="txtLimMundoyMin")
    labelLimMundoyMax = ttk.Label(t2.sub_frame, text="Y max")
    txtLimMundoyMax = ttk.Entry(t2.sub_frame, name="txtLimMundoyMax")

    labelLimPlanoProj = ttk.Label(t2.sub_frame, text="Plano de projeção", font="-weight bold -size 9")
    labelLimPlanoProjxMin = ttk.Label(t2.sub_frame, text="X min")
    txtLimPlanoProjxMin = ttk.Entry(t2.sub_frame, name="txtLimPlanoProjxMin")
    labelLimPlanoProjxMax = ttk.Label(t2.sub_frame, text="X max")
    txtLimPlanoProjxMax = ttk.Entry(t2.sub_frame, name="txtLimPlanoProjxMax")
    labelLimPlanoProjyMin = ttk.Label(t2.sub_frame, text="Y min")
    txtLimPlanoProjyMin = ttk.Entry(t2.sub_frame, name="txtLimPlanoProjyMin")
    labelLimPlanoProjyMax = ttk.Label(t2.sub_frame, text="Y max")
    txtLimPlanoProjyMax = ttk.Entry(t2.sub_frame, name="txtLimPlanoProjyMax")

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

    rbProjecao.trace('w', lerRadioButton)

    root.mainloop()