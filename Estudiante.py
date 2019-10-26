
class Estudiante:

    def __init__(self, dni, nombre, apellido, institucion, *args, **kwargs):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.institucion = institucion        

        if kwargs['telefono']:
            self.telefono = kwargs['telefono']

    def get_dni(self):
        return self.dni

    def get_nombre(self):
        return self.nombre
    
    def get_apellido(self):
        return self.apellido
    
    def get_institucion(self):
        return self.institucion
    
    def get_telefono(self):
    	return self.telefono
