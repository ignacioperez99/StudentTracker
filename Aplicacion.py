from tkinter import Tk, messagebox as mb, Menu, Listbox, StringVar
from tkinter.ttk import Frame, Label, Entry, Button, Notebook, Combobox
from Tabla import Tabla
from Cursante import Cursante, FormCreateCursante, FormDetailsCursante
from Docente import Docente, FormCreateDocente, FormDetailsDocente 
""" from Inscripto import Inscripto, FormInscripto  """
from Curso import Curso, FormCreateCurso, FormDetailsCurso
import sqlite3


class MainApplication(Tk):

    def __init__(self, *args, **kwargs):
        global connection
        self.cursor = connection.cursor()

        # Establece las configuraciones de la ventana principal
        self.root = Tk()
        self.root.title("Sistema de Gestión de Alumnos")
        self.root.geometry("1010x600")
        self.root.resizable(0,0)
        self.root.option_add("*tearOff", False)

        self.root.bind("<FocusIn>", self.update_tables)

        self.create_widgets()

        self.root.deiconify()
        self.root.mainloop()

    def create_widgets(self):
        global connection 

        # Crea la barra menú con sus opciones
        toolbar = Menu(self.root)
        self.root["menu"] = toolbar

        self.menu_opciones = Menu(toolbar)
        self.menu_ayuda = Menu(toolbar)
        toolbar.add_cascade(menu=self.menu_opciones, label="Acciones")
        toolbar.add_cascade(menu=self.menu_ayuda, label="Ayuda")
                 
        self.menu_opciones.add_command(label="Cerrar sesión",
                                       command=self.update_tables)                                       


        tabController = Notebook(self.root)
        tabController.grid(column=0, row=0)

        self.frameInicio = Frame(tabController, padding=(10,10))
        tabController.add(self.frameInicio, text="Inicio")

        self.frameCursantes = Frame(tabController, padding=(10,10))
        tabController.add(self.frameCursantes, text="Alumnos")

        self.frameDocentes = Frame(tabController, padding=(10,10))
        tabController.add(self.frameDocentes, text="Docentes")

        self.frameCursos = Frame(tabController, padding=(10,10))
        tabController.add(self.frameCursos, text="Cursos")


        self.formCreateCursante = FormCreateCursante()
        btn_nuevoCursante = Button(self.frameCursantes, text="[+] Nuevo estudiante",
                                command=self.formCreateCursante.show)
        btn_nuevoCursante.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tableCursantesFrame = Frame(self.frameCursantes, relief="groove", padding=(5,5))
        tableCursantesFrame.grid(row=1, column=0, columnspan=980)                                

        self.tableCursantes = Tabla(tableCursantesFrame, FormDetailsCursante(),
                                   960, 420)
        

        self.formCreateDocente = FormCreateDocente()
        btn_nuevoDocente = Button(self.frameDocentes, text="[+] Nuevo docente",
                                command=self.formCreateDocente.show)
        btn_nuevoDocente.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tableDocentesFrame = Frame(self.frameDocentes, relief="groove", padding=(5,5))
        tableDocentesFrame.grid(row=1, column=0, columnspan=980)

        self.tableDocentes = Tabla(tableDocentesFrame, FormDetailsDocente(),
                                   980, 420, {"dni":15, "telefono":15, "titulo":30})


        self.formCreateCurso = FormCreateCurso()
        btn_nuevoCurso = Button(self.frameCursos, text="[+] Nuevo curso",
                                command=self.formCreateCurso.show)
        btn_nuevoCurso.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tableCursosFrame = Frame(self.frameCursos, relief="groove", padding=(5,5))
        tableCursosFrame.grid(row=1, column=0, columnspan=970)

        self.tableCursos = Tabla(tableCursosFrame, FormDetailsCurso(),
                                  980, 420, {"nombre":40})


        lbl_curso = Label(self.frameInicio, text="Seleccione el curso:")
        lbl_curso.grid(row=0, column=0, columnspan=10, pady=5)

        self.curso = StringVar()
        values = [dict(item)["codigo"] for item in Curso.get_all()["data"]]
        cb_curso = Combobox(self.frameInicio, textvariable=self.curso, width=20,
                               values=values, state="readonly")
        cb_curso.current(0)
        cb_curso.grid(row=1, column=0, columnspan=20, pady=(0,15))

        """ self.tablaInicio = Tabla(self.frameInicio,) """

        self.tipo = StringVar()
        cb_tipos = Combobox(self.frameInicio, textvariable=self.tipo, width=20,
                            values=("Alumnos", "Docentes"))
        cb_tipos.current(0)
        cb_tipos.grid(row=1, column=60, columnspan=20, pady=(0,15))

    def update_tables(self, *args):
        self.tableCursos.check_update()
        self.tableCursantes.check_update()
        self.tableDocentes.check_update()

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
            mb.showerror("Datos inválidos", "El usuario y/o la contraseña son incorrectos.")

if __name__ == "__main__":
    connection = None

    try:
        connection = sqlite3.connect("./Database.db")
        connection.row_factory = sqlite3.Row

    except Exception as e:
        mb.showerror("Error de base de datos", e)
    
    Curso.connection = connection
    Cursante.connection = connection
    Docente.connection = connection

    """ win_login = WinLogin()
    
    if win_login.accepted: """
    app = MainApplication()
