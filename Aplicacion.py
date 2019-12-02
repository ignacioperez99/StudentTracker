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
import sqlite3


class MainApplication(Tk):

    def __init__(self, *args, **kwargs):
        # Establace las configuraciones de la ventana principal
        self.root = Tk()
        self.root.title("Sistema de Gestión de Alumnos")
        self.root.geometry("1010x585")
        self.root.resizable(0,0)
        self.root.option_add("*tearOff", False)

        self.root.bind("<FocusIn>", self.update_tablas)

        self.create_widgets()

        self.root.deiconify()
        self.root.mainloop()

    def create_widgets(self):

        # Crea la barra menú con sus opciones
        """ toolbar = Menu(self.root)
        self.root["menu"] = toolbar

        self.menu_opciones = Menu(toolbar)
        self.menu_ayuda = Menu(toolbar)
        toolbar.add_cascade(menu=self.menu_opciones, label="Acciones")
        toolbar.add_cascade(menu=self.menu_ayuda, label="Ayuda")
                 
        self.menu_opciones.add_command(label="Cerrar sesión",
                                       command=self.update_tablas)   """                                     


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


        formCreateCursante = FormCreateCursante()
        btn_nuevoCursante = Button(frameCursantes, text="[+] Nuevo estudiante",
                                command=formCreateCursante.show)
        btn_nuevoCursante.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tablaCursantesFrame = Frame(frameCursantes, relief="groove", padding=(5,5))
        tablaCursantesFrame.grid(row=1, column=0, columnspan=980)                                

        self.tablaCursantes = Tabla(tablaCursantesFrame, FormDetailsCursante())
        

        formCreateDocente = FormCreateDocente()
        btn_nuevoDocente = Button(frameDocentes, text="[+] Nuevo docente",
                                command=formCreateDocente.show)
        btn_nuevoDocente.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tablaDocentesFrame = Frame(frameDocentes, relief="groove", padding=(5,5))
        tablaDocentesFrame.grid(row=1, column=0, columnspan=980)

        self.tablaDocentes = Tabla(tablaDocentesFrame, FormDetailsDocente(),
                                   columns_width={"dni":15, "telefono":15, "titulo":30})


        formCreateCurso = FormCreateCurso()
        btn_nuevoCurso = Button(frameCursos, text="[+] Nuevo curso",
                                command=formCreateCurso.show)
        btn_nuevoCurso.grid(row=0, column=0, columnspan=30, pady=(5,10))

        tablaCursosFrame = Frame(frameCursos, relief="groove", padding=(5,5))
        tablaCursosFrame.grid(row=1, column=0, columnspan=970)

        self.tablaCursos = Tabla(tablaCursosFrame, FormDetailsCurso(),
                                 columns_width={"nombre":40})


        lbl_curso = Label(frameInicio, text="Seleccione el curso:")
        lbl_curso.grid(row=0, column=0)

        self.id_curso = StringVar()
        values = [dict(item)["codigo"] for item in Curso.get_all()["data"]]
        cb_curso = Combobox(frameInicio, textvariable=self.id_curso, width=20,
                               values=values, state="readonly")
        cb_curso.current(0)
        cb_curso.grid(row=1, column=0)



        tabFrameCurso = Notebook(frameInicio)
        tabFrameCurso.grid(row=2, column=0)

        frameInscriptos = Frame(tabFrameCurso, padding=(10,10))
        tabFrameCurso.add(frameInscriptos, text="Inscriptos")

        frameCurDoc = Frame(tabFrameCurso, padding=(10,10))
        tabFrameCurso.add(frameCurDoc, text="Docentes")


        self.formAddAlumno = FormInscriptos("add")
        self.formRemoveAlumno = FormInscriptos("remove")
        self.formAsistencias = FormAsistencias()
        self.formAsistencias.id_curso = self.id_curso.get()

        btn_add_cursante = Button(frameInscriptos, text="[+] Agregar", width=15,
                               command=lambda: self.formAddAlumno.show(self.id_curso.get()))
        btn_add_cursante.grid(row=0, column=0, columnspan=15)

        btn_remove_cursante = Button(frameInscriptos, text="[-] Remover", width=15,
                               command=lambda: self.formRemoveAlumno.show(self.id_curso.get()))
        btn_remove_cursante.grid(row=0, column=16, columnspan=15)

        frameTablaInscriptos = Frame(frameInscriptos, relief="groove", padding=(5,5))
        self.tablaInscriptos = Tabla(frameTablaInscriptos, self.formAsistencias,
                                     height=400)
        frameTablaInscriptos.grid(row=1, column=0, columnspan=150, pady=10) 

        btn_asistencia = Button(frameInscriptos, text="Cargar asistencia", width=25,
                                command=lambda: self.formAsistencias.show(self.id_curso.get()))
        btn_asistencia.grid(row=0, column=100, columnspan=25)

        data = {"nombre": "Kevin Edgardo",
                "apellido": "Juarez Desch",
                "nombre_curso": "Introducción a nuevas tecnologías"}

        btn_certificate = Button(frameInscriptos, text="Generar certificados", width=25,
                               command=lambda: self.generate_certificate(data))
        btn_certificate.grid(row=0, column=126, columnspan=25) 


        self.formAddDocente = FormDocentesCurso("add")
        self.formRemoveDocente = FormDocentesCurso("remove")

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

    def update_tablas(self, *args):
        self.tablaCursos.check_update()
        self.tablaCursantes.check_update()
        self.tablaDocentes.check_update()
        self.tablaDocentesMiembro.update_table()
        self.tablaInscriptos.update_table()

    def generate_certificate(self, data):
        registerFont(TTFont('Calibri', 'calibri.ttf'))
        registerFont(TTFont('Calibri-Bold', 'calibrib.ttf'))

        name = data["nombre"].upper()
        """ dni = data["dni"] """
        surname = data["apellido"].upper()
        course_name = data["nombre_curso"].upper()
        pdf_name = f"{course_name}_{surname}_{name}.pdf"
        
        c = canvas.Canvas(pdf_name, pagesize=landscape(letter))

        logo = "logo_utn.png"
        c.drawImage(logo, 260, 450, width=250, height=110)

        # Título
        c.setFont("Calibri-Bold", 35)
        c.drawCentredString(390, 400, "CERTIFICADO DE FINALIZACIÓN")
        c.setFont("Calibri", 24)
        c.drawCentredString(390, 350, "Este certificado se presenta a:")
        # Nombre completo
        c.setFont("Calibri-Bold", 30)
        c.drawCentredString(390, 295, f"{name} {surname}")

        # Por haber completado
        c.setFont("Calibri", 24)
        c.drawCentredString(390, 150, "Por completar el curso:")

        # Nombre del curso
        c.setFont("Calibri", 20)
        c.drawCentredString(390, 110, course_name)

        c.showPage()

        c.save()

class WinLogin(Tk):

    def __init__(self, *args, **kwargs):
        global connection
        self.cursor = connection.cursor() 

        self.accepted = False

        # Establace las configuraciones de la ventana de logueo
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
        connection = sqlite3.connect("./algo.db")
        connection.row_factory = sqlite3.Row

    except Exception as e:
        mb.showerror("Error de base de datos", e)
    
    Tabla.connection    = connection
    Curso.connection    = connection
    Cursante.connection = connection
    Docente.connection  = connection

    """ win_login = WinLogin()
    
    if win_login.accepted: """
    app = MainApplication()
