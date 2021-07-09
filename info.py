import tkinter as tk
from tkinter import Frame, ttk
from tkinter.constants import N, S, W 


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

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')


if __name__ == "__main__":
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(str(int(width*0.2))+"x"+str(height))

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

    labelCg.grid(row=1, column=1, padx=1, pady=5)
    txtCg.grid(row=1, column=2, padx=1, pady=5)
    labelRaioBase.grid(row=2, column=1, padx=1, pady=5)
    txtRaioBase.grid(row=2, column=2, padx=1, pady=5)
    labelRaioTopo.grid(row=3, column=1, padx=1, pady=5)
    txtRaioTopo.grid(row=3, column=2, padx=1, pady=5)
    labelNumLados.grid(row=4, column=1, padx=1, pady=5)
    txtNumLados.grid(row=4, column=2, padx=1, pady=5)
    labelAltura.grid(row=5, column=1, padx=1, pady=5)
    txtAltura.grid(row=5, column=2, padx=1, pady=5)

    t2 = ToggledFrame(root, text='Projeção', relief="raised", borderwidth=1)
    t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    labelTipoProjecao = ttk.Label(t2.sub_frame, text="Tipo de projeção")
    rbAxonometrica = ttk.Radiobutton(t2.sub_frame, text="Axonométrica", value=1)
    rbPerspectiva = ttk.Radiobutton(t2.sub_frame, text="Perspectiva", value=2)
    labelVRP = ttk.Label(t2.sub_frame, text="VRP", width=4)
    labelVRPx = ttk.Label(t2.sub_frame, text="X")
    txtVRPx = ttk.Entry(t2.sub_frame, name="txtVRPx")
    labelVRPy = ttk.Label(t2.sub_frame, text="Y")
    txtVRPy= ttk.Entry(t2.sub_frame, name="txtVRPy")
    labelVRPz = ttk.Label(t2.sub_frame, text="Z")
    txtVRPz = ttk.Entry(t2.sub_frame, name="txtVRPz")

    labelTipoProjecao.grid(row=1, column=1, padx=1, pady=2)
    rbAxonometrica.grid(row=2, column=1, padx=5, pady=2)
    rbPerspectiva.grid(row=2, column=2, padx=5, pady=2)
    labelVRP.grid(row=3, column=1, padx=1, pady=1, ipadx=3, sticky=W, columnspan=1)
    labelVRPx.grid(row=3, column=2, padx=1, pady=1, ipadx=3, sticky=W, columnspan=1)
    txtVRPx.grid(row=3, column=3, padx=1, pady=1, ipadx=3, sticky=W, columnspan=1)
    labelVRPy.grid(row=4, column=1, padx=1, pady=1)
    txtVRPy.grid(row=4, column=2, padx=1, pady=1)
    labelVRPz.grid(row=5, column=1, padx=1, pady=1)
    txtVRPz.grid(row=5, column=2, padx=1, pady=1)

    root.mainloop()