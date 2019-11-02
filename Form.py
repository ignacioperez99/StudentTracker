# Clase padre de la cual heredan todos los formularios.
# Permite reutilizar código, si no existiera, cada formulario
# debería implementar cada uno de estos métodos. Pero de esta
# forma cuando se invocan estos métodos en las clases hijas
# y las mismas no los sobre escribieron, se los busca en la 
# clase padre.

class Form():

    def __init__(self, fields, *args, **kwargs):
        self.fields = fields
        self.modified = False
        self.id_register = None

    def set_id_register(self, id_register):
        self.id_register = id_register

    def need_update(self):
        return self.modified

    def updated(self):
        self.modified = False
    
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
            self.fields[key].insert(0, str(dict_data[key]))

    def clean_fields(self):
        # Vacía el contenido de todos los campos
        for key in self.fields:
            self.fields[key].delete(0,'end')