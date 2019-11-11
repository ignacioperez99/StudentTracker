from tkinter import Toplevel
from Cursante import StudentForm
from Docente import TeacherForm
from Curso import CourseForm
import sqlite3

class Viewer:

    def __init__(self, title, class_type, *args, **kwargs):
        self.class_type = class_type

        # Al momento de crear la ventana, también la oculta
        self.root = Toplevel()
        self.root.withdraw()
        self.root.title(title)
        self.root.resizable(0,0)

        # Al cerrar la ventana, esta sólo se ocultará.
        # Esto evita crearla cada vez que se la necesita.
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

        # Dependiendo del nombre de la tabla va a ser el 
        # tipo de formulario que va a utilizar. Esto permite
        # reutilizar código.
        self.class_type.create_form(self.root)

    def show(self, id_register):
        register = self.class_type.get_register(id_register)

        # Se limpian los campos y se carga la nueva
        # info, mediante el llamado a la clase padre 'Form'
        self.class_type.clean_fields()
        self.class_type.load_data(register)

        # Se muestra la ventana
        self.root.deiconify()

    def hide(self):
        # Se oculta la ventana
        self.root.withdraw()
        