from tkinter import Toplevel
from Cursante import StudentForm
from Docente import TeacherForm
from Curso import CourseForm
import sqlite3

class Viewer:

    def __init__(self, title, table_name, connection, *args, **kwargs):
        self.cursor = connection.cursor()
        self.table = table_name

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
        if table_name == "Cursante":
            self.form = StudentForm(self.root, connection, "details")

        elif table_name == "Docente":
            self.form = TeacherForm(self.root, connection, "details")
        
        elif table_name == "Curso":
            self.form = CourseForm(self.root, connection, "details")

    def show(self, id_register):
        # Se obtiene un registro en base al id
        # y al nombre de la tabla
        sql = "select * from {} where codigo = (?)".format(self.table)

        # Se debe poner una coma aunque haya sólo            |
        # un argumento para que sea un objeto iterable       V
        register = self.cursor.execute(sql, (id_register,))
        register = register.fetchone()

        self.form.set_id_register(id_register)

        # Se limpian los campos y se carga la nueva
        # info, mediante el llamado a la clase padre 'Form'
        self.form.clean_fields()
        self.form.load_data(register)

        # Se muestra la ventana
        self.root.deiconify()

    def hide(self):
        # Se oculta la ventana
        self.root.withdraw()
        