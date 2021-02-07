from tkinter import Toplevel
# Clase padre de la cual heredan todos los formularios.
# Permite reutilizar código, si no existiera, cada formulario
# debería implementar cada uno de estos métodos. Pero de esta
# forma cuando se invocan estos métodos en las clases hijas
# y las mismas no los sobre escribieron, se los busca en la 
# clase padre.

class Form():

    def __init__(self):
        # Al momento de crear la ventana, también la oculta
        self.root = Toplevel()
        self.root.withdraw()
        self.root.resizable(0,0)

        # Al cerrar la ventana, esta sólo se ocultará.
        # Esto evita crearla cada vez que se la necesita.
        self.root.protocol("WM_DELETE_WINDOW", self.hide)
        
        self.fields = {}
    
    def show(self):
        # Se muestra la ventana
        self.root.deiconify()

    def hide(self):
        # Se oculta la ventana
        self.root.withdraw()

    def set_fields(self, fields):
        self.fields = fields

    def set_title(self, title):
        self.root.title(title)

    def get_data(self):
        # Retorna un diccionario con la info
        # contenida en cada campo
        data = []

        for item in self.fields.values():
            i = item.get().strip()
            data.append(i if i and not i == '' else None)

        return data

    def load_data(self, data):
        # Inserta en cada campo
        # la información que el es enviada.
        dict_data = dict(data)
        
        for key in self.fields:
            self.fields[key].set(dict_data[key])

    def clean_fields(self):
        # Vacía el contenido de todos los campos
        for key in self.fields:
            self.fields[key].set("")

    def validate_int(self, var, *args):     
        value = var.get()

        if not value.isdigit():
            var.set("".join(x for x in value if x.isdigit()))

    def validate_dni(self, var, *args):
        value = var.get()
        
        if not len(value)<8:
            var.set(value[:8])

        self.validate_int(var)

    def validate_phone(self, var, *args):
        value = var.get()
        
        if not value.isdigit():
            var.set("".join(x for x in value if x.isdigit()))

    def validate_str(self, var, *args):
        value = var.get()
        
        if not value.isalpha():
            var.set("".join(x for x in value if x.isalpha() or x.isspace()))

    def validate_place(self, var, *args):
        value = var.get()
        
        if not value.isalnum():
            var.set("".join(x for x in value if x.isalnum() or x.isspace()))