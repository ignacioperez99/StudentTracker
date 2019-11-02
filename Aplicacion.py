from tkinter import Tk, messagebox, Menu
from tkinter.ttk import Frame, Label, Entry, Button, Notebook
from Tabla import Table
from Cursante import StudentForm
from Docente import TeacherForm
from Curso import CourseForm
from Viewer import Viewer
import sqlite3


class MainApplication(Tk):

    def __init__(self, *args, **kwargs):
        global connection
        self.cursor = connection.cursor()

        # Establece las configuraciones de la ventana principal
        self.root = Tk()
        self.root.title("Sistema de Gestión de Alumnos")
        self.root.geometry("1200x500")
        self.root.resizable(0,0)
        self.root.option_add("*tearOff", False)

        self.root.bind("<FocusIn>", self.update_tables)

        self.create_widgets()

        self.root.deiconify()
        self.root.mainloop()

    def create_widgets(self):
        global connection 

        # Crea la barra menú con sus opciones
        """ toolbar = Menu(self.root)
        self.root["menu"] = toolbar

        self.menu_opciones = Menu(toolbar)
        self.menu_ayuda = Menu(toolbar)
        toolbar.add_cascade(menu=self.menu_opciones, label="Acciones")
        toolbar.add_cascade(menu=self.menu_ayuda, label="Ayuda")
                 
        self.menu_opciones.add_command(label="Actualizar",
                                       command=self.update_tables) """


        tabController = Notebook(self.root)
        tabController.grid(column=0, row=0)

        self.studentsFrame = Frame(tabController, padding=(10,10))
        tabController.add(self.studentsFrame, text="Alumnos")

        self.teachersFrame = Frame(tabController, padding=(10,10))
        tabController.add(self.teachersFrame, text="Docentes")

        self.coursesFrame = Frame(tabController, padding=(10,10))
        tabController.add(self.coursesFrame, text="Cursos")


        tableStudentsFrame = Frame(self.studentsFrame, relief="groove", padding=(5,5))
        tableStudentsFrame.grid(row=0, column=15, padx=10)                                

        self.tableStudents = Table(tableStudentsFrame, "Cursante", 
                                   Viewer("Detalles del Alumno", "Cursante", connection),
                                   850, 420,
                                   connection)

        self.form_students = StudentForm(self.studentsFrame, connection, "create")
        

        tableTeachersFrame = Frame(self.teachersFrame, relief="groove", padding=(5,5))
        tableTeachersFrame.grid(row=0, column=15, padx=10)

        self.tableTeachers = Table(tableTeachersFrame, "Docente",
                                   Viewer("Detalles del Docente", "Docente", connection),
                                   850, 420,
                                   connection, {"dni":15, "telefono":15, "titulo":30})

        self.form_teachers = TeacherForm(self.teachersFrame, connection, "create")
        

        tableCoursesFrame = Frame(self.coursesFrame, relief="groove", padding=(5,5))
        tableCoursesFrame.grid(row=0, column=15, padx=10)

        self.tableCourses = Table(tableCoursesFrame, "Curso",
                                  Viewer("Detalles del Curso", "Curso", connection),
                                  850, 420,
                                  connection, {"nombre":40})

        self.form_courses = CourseForm(self.coursesFrame, connection, "create")

    def update_tables(self, *args, **kwargs):
        self.tableCourses.check_update(self.form_courses)
        self.tableStudents.check_update(self.form_students)
        self.tableTeachers.check_update(self.form_teachers)

class WinLogin(Tk):

    def __init__(self, *args, **kwargs):
        global connection
        self.cursor = connection.cursor() 

        self.accepted = False

        # Establece las configuraciones de la ventana de logueo
        self.root = Tk()
        self.root.title("Inicio de sesión")
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        lbl_user = Label(self.root, text="Usuario: ")
        lbl_user.grid(row=0, column=0, padx=(20,10), pady=(10,0))

        self.e_user = Entry(self.root, width=25)
        self.e_user.grid(row=0, column=1, padx=(10,20), pady=(20,10)) 
        self.e_user.focus_set()

        lbl_password = Label(self.root, text="Contraseña: ")
        lbl_password.grid(row=2, column=0, padx=(20,10))

        self.e_password = Entry(self.root, width=25)
        self.e_password.grid(row=2, column=1, padx=(10,20), pady=10) 

        btn_login = Button(self.root, text="Ingresar", command=self.login)
        btn_login.grid(row=3, column=0, columnspan=3, padx=10, pady=(5,20))

        self.root.mainloop()


    def login(self):
        # Busca el administrador que posea el usuario y la contraseña proporcionados.
        self.cursor.execute("select * from Administrador where usuario = (?) and contrasena = (?)", (self.e_user.get(), self.e_password.get()))
        
        # Si lo encontró, completa el logueo. Caso contrario, informa el error.
        if self.cursor.fetchone():
            self.accepted = True
            self.root.destroy()
        else:
            messagebox.showerror("Datos inválidos", "El usuario y/o la contraseña son incorrectos.")

if __name__ == "__main__":
    connection = None

    try:
        connection = sqlite3.connect("./Database.db")
        connection.row_factory = sqlite3.Row

    except Exception as e:
        messagebox.showerror("Error de base de datos", e)

    """ win_login = WinLogin()
    
    if win_login.accepted: """
    app = MainApplication()
