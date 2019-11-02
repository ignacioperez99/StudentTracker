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


class Table:

    def __init__(self, root, table_name, viewer, width, height, connection, columns_width=None):
        self.conn = connection
        self.viewer = viewer
        self.table_name = table_name
        self.columns_width = columns_width
    
        # Se inicializan ambos scrollbars para el Canvas
        vscrollbar = AutoScrollbar(root)
        vscrollbar.grid(row=0, column=1, sticky="N"+"S")
        hscrollbar = AutoScrollbar(root, orient="horizontal")
        hscrollbar.grid(row=1, column=0, sticky="E"+"W")


        # Se inicializa el Canvas y se le
        # agregan los scrollbars
        canvas = Canvas(root, width=width, height=height, 
                             highlightthickness=0, 
                             yscrollcommand=vscrollbar.set,
                             xscrollcommand=hscrollbar.set)
        canvas.grid(row=0, column=0, sticky="N"+"S"+"E"+"W")

        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        # Permite al canvas expandirse
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Se crea el contenido del canvas
        self.root = Frame(canvas)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.update()

        canvas.create_window(0, 0, anchor="nw", window=self.root)

        self.root.update_idletasks()

        canvas.config(scrollregion=canvas.bbox("all"))

    def check_update(self, *args, **kwargs):
        update = False

        if self.viewer.form.need_update():
            update = True
            self.update()
            self.viewer.form.updated()

        if not update:
            for form in args:
                update = form.need_update()
                if update:
                    self.update()
                    form.updated()
                    return

    def update(self):
        print(f"se updateo {self.table_name}")
        if self.root.winfo_children():
            self.root.winfo_children()[0].destroy()

        cur = self.conn.cursor()
        # Se obtiene la tabla completa de la base de datos
        data = cur.execute("select * from {}".format(self.table_name))

        frame = Frame(self.root)

        # Crea la tabla iterando sobre cada campo de
        # cada uno de los registros de la consulta.
        for item in data.fetchall():
            row = Frame(frame)

            for field in dict(item):
                if field == 'codigo':
                    btn_id = Button(row, text="Ver", command= lambda index=item[field]: self.viewer.show(index))
                    btn_id.pack(side="right")
                else:
                    # Se utiliza un operador ternario para hacer más configurable
                    # a la tabla, permitiendo modificar el tamaño de las columnas
                    entry = Entry(row, width=self.columns_width[field] 
                                                if self.columns_width 
                                                and field in self.columns_width 
                                                else 20)
                    entry.pack(side="left")
                    entry.insert(0, str(item[field]))
                    entry.config(state="readonly")

            row.pack(side="top")

        frame.pack()