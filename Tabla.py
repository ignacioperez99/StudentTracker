from tkinter import Canvas
from tkinter.ttk import Scrollbar, Entry, Button, Frame

class AutoScrollbar(Scrollbar):
    # Barra de desplazamiento que se oculta cuando no se
    # necesita. Sólo funciona con el layout grid.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)


class Tabla:

    def __init__(self, root, viewer, btn=True, width=960, height=420, columns_width=None):
        self.viewer = viewer
        self.columns_width = columns_width
        self.btn = btn
    
        # Se inicializan ambos scrollbars para el Canvas
        vscrollbar = AutoScrollbar(root)
        vscrollbar.grid(row=0, column=1, sticky="N"+"S")
        hscrollbar = AutoScrollbar(root, orient="horizontal")
        hscrollbar.grid(row=1, column=0, sticky="E"+"W")


        # Se inicializa el Canvas y se le
        # agregan los scrollbars
        self.canvas = Canvas(root, width=width, height=height, 
                             highlightthickness=0, 
                             yscrollcommand=vscrollbar.set,
                             xscrollcommand=hscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="N"+"S"+"E"+"W")

        # Se establece la acción de cada scrollbar
        # sobre el canvas correspondientemente
        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)

        # Permite al self.canvas expandirse
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Se crea el contenido del self.canvas
        self.root = Frame(self.canvas)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        self.update_table()

        self.canvas.create_window(0, 0, anchor="nw", window=self.root)

    def check_update(self):
        '''
        Verifica si es necesario actualizar la 
        tabla visualmente y la actualiza.
        '''
        if self.viewer.is_update():
            self.update_table()
            self.viewer.updated()

    def update_table(self):
        '''
        Actualiza la información que se muestra en la
        tabla con lo actualizado de la base de datos.
        '''
        
        # Destruye todo los componentes que se encuentren en
        # marco principal (la tabla) para poder generarlos
        # nuevamente con la información actualizada.
        for c in self.root.winfo_children():
            c.destroy()

        self.viewer.hide()

        # Se obtiene la tabla completa de la base de datos
        data =  self.viewer.get_all()["data"]
        names = self.viewer.get_all()["names"]

        # Se crea la primer fila que contiene los
        # nombres de las columnas
        frameNames = Frame(self.root)
        for name in names:
            # Se utiliza una operación ternaria (se utilizan varias
            # en la app, simplifican el código) para determinar si
            # es necesario aplicar un tamaño provisto de largo de columna
            e = Entry(frameNames, width=self.columns_width[name] 
                                        if self.columns_width 
                                        and name in self.columns_width 
                                        else 20)
            e.insert(0, str(name).replace("_"," ").capitalize())
            e.config(state="readonly")
            e.pack(side="left")
        frameNames.pack(side="top", padx=(0,75))
        
        frame = Frame(self.root)
            
        # Crea la tabla iterando sobre cada campo de
        # cada uno de los registros de la consulta.
        for item in data:
            row = Frame(frame)
            for field in dict(item):
                if self.btn and field == 'codigo':
                    btn_id = Button(row, text="Ver", command= lambda index=item[field]: self.viewer.show(index))
                    btn_id.pack(side="right")
                
                # Se utiliza un operador ternario para hacer más configurable
                # a la tabla, permitiendo modificar el tamaño de las columnas
                entry = Entry(row, width=self.columns_width[field] 
                                            if self.columns_width 
                                            and field in self.columns_width 
                                            else 20)
                entry.pack(side="left")
                entry.insert(0, str(item[field]))
                entry.config(state="readonly")

            if self.btn:
                row.pack(side="top")
            else:
                row.pack(side="top", padx=(0,75))

        frame.pack()

        # Se fija el area de desplazamiento de la tabla en
        # base a la cantidad de filas que posea.
        height = (len(frame.winfo_children())*25)+25
        self.canvas.config(scrollregion=(0,0,0,height))