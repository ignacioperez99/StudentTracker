from tkinter import Tk, messagebox as mb, Menu, Listbox, StringVar
from tkinter.ttk import Frame, Label, Entry, Button, Notebook, Combobox
from Tabla import Tabla
from Cursante import Cursante, FormCreateCursante, FormDetailsCursante
from Docente import Docente, FormCreateDocente, FormDetailsDocente 
from Curso import Curso, FormCreateCurso, FormDetailsCurso, FormDocentesCurso, FormInscriptos, FormAsistencias
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from MyPDF import generar_pdf
import sqlite3


class MainApplication(Tk):

    def __init__(self, *args, **kwargs):
        '''
        Establace las configuraciones de la ventana principal
        '''
        self.root = Tk()
        self.root.title("Sistema de Gestión de Alumnos")
        self.root.geometry("1010x585")
        self.root.resizable(0,0)
        self.root.option_add("*tearOff", False)

        # Ejecuta la función de actualizar las tablas
        # cuando la ventana principal obtiene el foco
        self.root.bind("<FocusIn>", self.update_tablas)

        self.create_widgets()

        # Le otorga el foco a la ventana principal
        self.root.deiconify()
        # La mantiene en ejecución
        self.root.mainloop()

    def create_widgets(self):
        '''
        Crea todos los componentes de la ventana principal
        '''
        #### TABS ####
        tabController = Notebook(self.root)
        tabController.grid(column=0, row=0)

        frameInicio = Frame(tabController, padding=(10,10))
        tabController.add(frameInicio, text="Inicio")

        frameCursantes = Frame(tabController, padding=(10,10))
        tabController.add(frameCursantes, text="Alumnos")

        frameDocentes = Frame(tabController, padding=(10,10))
        tabController.add(frameDocentes, text="Docentes")

        frameCursos = Frame(tabController, padding=(10,10))
        tabController.add(frameCursos, text="Cursos")

        #### TAB ALUMNOS ####
        formCreateCursante = FormCreateCursante()
        btn_nuevoCursante = Button(frameCursantes, text="[+] Nuevo estudiante",
                                command=formCreateCursante.show)
        btn_nuevoCursante.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tablaCursantesFrame = Frame(frameCursantes, relief="groove", padding=(5,5))
        tablaCursantesFrame.grid(row=1, column=0, columnspan=980)                                

        self.tablaCursantes = Tabla(tablaCursantesFrame, FormDetailsCursante())
        
        #### TAB DOCENTES ####
        formCreateDocente = FormCreateDocente()
        btn_nuevoDocente = Button(frameDocentes, text="[+] Nuevo docente",
                                command=formCreateDocente.show)
        btn_nuevoDocente.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tablaDocentesFrame = Frame(frameDocentes, relief="groove", padding=(5,5))
        tablaDocentesFrame.grid(row=1, column=0, columnspan=980)

        self.tablaDocentes = Tabla(tablaDocentesFrame, FormDetailsDocente(),
                                   columns_width={"dni":15, "telefono":15, "titulo":30})

        #### TAB CURSOS ####
        formCreateCurso = FormCreateCurso()
        btn_nuevoCurso = Button(frameCursos, text="[+] Nuevo curso",
                                command=formCreateCurso.show)
        btn_nuevoCurso.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tablaCursosFrame = Frame(frameCursos, relief="groove", padding=(5,5))
        tablaCursosFrame.grid(row=1, column=0, columnspan=970)

        self.tablaCursos = Tabla(tablaCursosFrame, FormDetailsCurso(),
                                 columns_width={"nombre":40})


        #### TAB INICIO ####
        lbl_curso = Label(frameInicio, text="Seleccione el curso:")
        lbl_curso.grid(row=0, column=0)

        self.id_curso = StringVar()
        values = [dict(item)["codigo"] for item in Curso.get_all()["data"]]
        cb_curso = Combobox(frameInicio, textvariable=self.id_curso, width=20,
                               values=values, state="readonly")
        cb_curso.current(0)
        cb_curso.grid(row=1, column=0)
        cb_curso.bind("<<ComboboxSelected>>", self.selection_changed)


        tabFrameCurso = Notebook(frameInicio)
        tabFrameCurso.grid(row=2, column=0)

        frameInscriptos = Frame(tabFrameCurso, padding=(10,10))
        tabFrameCurso.add(frameInscriptos, text="Inscriptos")

        frameCurDoc = Frame(tabFrameCurso, padding=(10,10))
        tabFrameCurso.add(frameCurDoc, text="Docentes")

        frameAsiastencias = Frame(tabFrameCurso, padding=(10,10))
        tabFrameCurso.add(frameAsiastencias, text="Asistencias")


        self.formAddAlumno = FormInscriptos("add")
        self.formRemoveAlumno = FormInscriptos("remove")
        self.formRemoveAlumno.id_curso = self.id_curso.get()

        btn_add_cursante = Button(frameInscriptos, text="[+] Agregar", width=15,
                               command=lambda: self.formAddAlumno.show(self.id_curso.get()))
        btn_add_cursante.grid(row=0, column=0, columnspan=15)

        btn_remove_cursante = Button(frameInscriptos, text="[-] Remover", width=15,
                               command=lambda: self.formRemoveAlumno.show(self.id_curso.get()))
        btn_remove_cursante.grid(row=0, column=16, columnspan=15)

        frameTablaInscriptos = Frame(frameInscriptos, relief="groove", padding=(5,5))
        self.tablaInscriptos = Tabla(frameTablaInscriptos, self.formRemoveAlumno,
                                     btn=False, height=400)
        frameTablaInscriptos.grid(row=1, column=0, columnspan=150, pady=10) 

        btn_certificate = Button(frameInscriptos, text="Generar certificados", width=25,
                               command=lambda: self.generate_certificate())
        btn_certificate.grid(row=0, column=126, columnspan=25) 


        self.formAddDocente = FormDocentesCurso("add")
        self.formRemoveDocente = FormDocentesCurso("remove")
        self.formRemoveDocente.id_curso = self.id_curso.get()

        btn_add_doc = Button(frameCurDoc, text="[+] Agregar", width=15,
                               command=lambda: self.formAddDocente.show(self.id_curso.get()))
        btn_add_doc.grid(row=0, column=0, columnspan=15)

        btn_remove_doc = Button(frameCurDoc, text="[-] Remover", width=15,
                               command=lambda: self.formRemoveDocente.show(self.id_curso.get()))
        btn_remove_doc.grid(row=0, column=16, columnspan=15) 

        frameTablaDocentesMiembro = Frame(frameCurDoc, relief="groove", padding=(5,5))
        self.tablaDocentesMiembro = Tabla(frameTablaDocentesMiembro, self.formRemoveDocente,
                                          btn=False, height=400)
        frameTablaDocentesMiembro.grid(row=1, column=0, columnspan=150, pady=10)


        self.formAsistencias = FormAsistencias()
        self.formAsistencias.id_curso = self.id_curso.get()

        btn_asistencia = Button(frameAsiastencias, text="Cargar asistencias", width=25,
                                command=lambda: self.formAsistencias.show(self.id_curso.get()))
        btn_asistencia.grid(row=0, column=0, columnspan=25)

        frameTablaAsistencias = Frame(frameAsiastencias, relief="groove", padding=(5,5))
        self.tablaAsistencias = Tabla(frameTablaAsistencias, self.formAsistencias,
                                      btn=False, height=400)
        frameTablaAsistencias.grid(row=1, column=0, columnspan=150, pady=10)

    def selection_changed(self, *args):
        '''
        Actualiza el ID del curso que se seleccionó en el combobox.
        '''
        self.formRemoveDocente.id_curso = self.id_curso.get()
        self.formRemoveAlumno.id_curso = self.id_curso.get()
        self.formAsistencias.id_curso = self.id_curso.get()

    def update_tablas(self, *args):
        '''
        Le indica a cada tabla que chequee si es
        necesario actualizar la información visual o
        que la actualice directamente dependiendo el caso
        '''
        self.tablaCursos.check_update()
        self.tablaCursantes.check_update()
        self.tablaDocentes.check_update()
        self.tablaDocentesMiembro.update_table()
        self.tablaInscriptos.update_table()
        self.tablaAsistencias.update_table()

    def generate_certificate(self):
        data = Curso.get_data_certificados(self.id_curso.get())
        
        for inscripto in data["asistieron"]:
            info = {"name": inscripto["nombre"].upper(),
                    "dni": inscripto["dni"],
                    "teachers": data["docentes"].upper(),
                    "course": data["curso"].upper(),
                    "dates": data["fechas"]}
            generar_pdf(info)

        cant_asist = len(data["asistieron"])
        mb.showinfo("Información", f"Se generó correctamente el certificado\na los {cant_asist} que asistieron al curso.")


class WinLogin(Tk):

    def __init__(self, *args, **kwargs):
        '''
        Se establecen las configuraciones de la ventana de logueo
        '''
        global connection
        self.cursor = connection.cursor() 

        self.accepted = False

        self.root = Tk()
        self.root.title("Inicio de sesión")
        self.root.resizable(0,0)
        # Cuando se genera el evento de eliminar la pantalla (cerrarla)
        # se destuye la ventana principal de la aplicación que estaba minimizada
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
        '''
        Realiza el proceso de logueo de un administrador
        '''
        # Busca el administrador que posea el usuario y la contraseña proporcionados.
        sql = '''SELECT * 
                 FROM `Administrador` 
                 WHERE usuario = (?) and contrasena = (?)'''
        self.cursor.execute(sql, (self.e_user.get(), self.e_password.get()))
        
        # Si lo encontró, completa el logueo. Caso contrario, informa el error.
        if self.cursor.fetchone():
            self.accepted = True
            self.root.destroy()
        else:
            mb.showerror("Datos inválidos", "El usuario y/o la contraseña son incorrectos.")

if __name__ == "__main__":
    connection = None

    try:
        # Se establece la conexión con la base de datos.
        connection = sqlite3.connect("./database.db")
        # Esto permite poder obtener los nombres de las columnas
        # de la tabla para poder armar de manera práctica y automática
        # las tablas visuales.
        connection.row_factory = sqlite3.Row

    except Exception as e:
        mb.showerror("Error de base de datos", e)
    
    Tabla.connection    = connection
    Curso.connection    = connection
    Cursante.connection = connection
    Docente.connection  = connection

    win_login = WinLogin()
    
    if win_login.accepted:
        app = MainApplication()
