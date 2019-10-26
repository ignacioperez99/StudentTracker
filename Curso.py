
class Curso:

    def __init__(self, nombre, carga, lugar, fecha_inicio, *args, **kwargs):
        self.nombre = nombre
        self.carga = carga
        self.lugar = lugar
        self.fecha_inicio = fecha_inicio
        
        if kwargs['fecha_fin']:
            self.fecha_fin = kwargs['fecha_fin']
    
        def get_nombre(self):
            return self.nombre

        def get_carga(self):
        	return self.carga
        
        def get_lugar(self):
        	return self.lugar
        
        def get_fecha_inicio(self):
        	return self.fecha_inicio

        def get_fecha_fin(self):
        	return self.fecha_fin
