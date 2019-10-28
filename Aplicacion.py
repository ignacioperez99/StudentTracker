import re, os, csv, tkinter as tk
from tkinter import Tk, messagebox, filedialog, Toplevel, Menu, Canvas, Frame as tkFrame
from tkinter.ttk import (Combobox, Frame, Label, Entry, Button,  
Notebook, LabelFrame, Scrollbar)
import sqlite3


class AutoScrollbar(Scrollbar):
    # Barra de desplazamiento que se oculta cuando no se
    # necesita. Sólo funciona con grid.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)


class Table:

    def __init__(self, root, data, *args, **kwargs):
        self.items = 0
    
        self.vscrollbar = AutoScrollbar(root)
        self.vscrollbar.grid(row=0, column=800, sticky="N"+"S")

        self.canvas = Canvas(root, width=850, height=420, 
                             highlightthickness=0, 
                             yscrollcommand=self.vscrollbar.set)
        self.canvas.grid(row=0, column=100, sticky="N"+"S"+"E"+"W")

        self.vscrollbar.config(command=self.canvas.yview)

        # Permite al canvas expandirse
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Se crea el contenido del canvas
        frame = Frame(self.canvas)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)

        # Crea la tabla iterando sobre cada campo de
        # cada uno de los registros de la consulta.
        for item in data:
            row = Frame(frame)
            for iCol, field in enumerate(item):
                
                if iCol == 0:
                    btn_id = Button(row, text="Ver")
                    btn_id.pack(side="right")

                else: 
                    entry = Entry(row)
                    entry.pack(side="left")
                    entry.insert(0, str(field))
                    entry.config(state="readonly")
            row.pack(side="top")

        self.canvas.create_window(0, 0, anchor="nw", window=frame)

        frame.update_idletasks()

        self.canvas.config(scrollregion=self.canvas.bbox("all"))


class TopStudent:

    def __init__(self, *args, **kwargs):
        self.root = Toplevel()
        self.root.withdraw()
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

        self.studentFrame = Frame(self.root, relief="groove", padding=(15,15))
        self.studentFrame.grid(column=0, row=0, padx=20, pady=20)

        lbl_dni = Label(self.studentFrame, text="DNI: ", width=10)
        lbl_dni.grid(row=0, column=0, columnspan=10)

        self.dni = Entry(self.studentFrame, width=40)
        self.dni.grid(row=1, column=0, columnspan=40, pady=(0,15))

        lbl_name = Label(self.studentFrame, text="Nombre: ", width=10)
        lbl_name.grid(row=2, column=0, columnspan=10)

        self.name = Entry(self.studentFrame, width=40)
        self.name.grid(row=3, column=0, columnspan=40, pady=(0,15))

        lbl_surname = Label(self.studentFrame, text="Apellido: ", width=10)
        lbl_surname.grid(row=4, column=0, columnspan=10)

        self.surname = Entry(self.studentFrame, width=40)
        self.surname.grid(row=5, column=0, columnspan=40, pady=(0,15))

        lbl_email = Label(self.studentFrame, text="Email: ", width=10)
        lbl_email.grid(row=6, column=0, columnspan=10)

        self.email = Entry(self.studentFrame, width=40)
        self.email.grid(row=7, column=0, columnspan=40, pady=(0,15))

        lbl_phone = Label(self.studentFrame, text="Teléfono: ", width=10)
        lbl_phone.grid(row=8, column=0, columnspan=10)

        self.phone = Entry(self.studentFrame, width=40)
        self.phone.grid(row=9, column=0, columnspan=40, pady=(0,15))

        lbl_institute = Label(self.studentFrame, text="Institución: ", width=10)
        lbl_institute.grid(row=10, column=0, columnspan=10)

        self.institute = Entry(self.studentFrame, width=40)
        self.institute.grid(row=11, column=0, columnspan=40, pady=(0,15))

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()

    
class MainApplication(Tk):

    def __init__(self, *args, **kwargs):
        # Establece las configuraciones de la ventana principal
        self.root = Tk()
        self.root.title("Sistema de Gestión de Alumnos")
        self.root.geometry("1200x500")
        self.root.resizable(0,0)
        self.root.option_add("*tearOff", False)

        self.cursor = connection.cursor()

        self.top_student = TopStudent()
        self.create_widgets()

        self.root.deiconify()
        self.root.mainloop()

    def create_widgets(self):
        # Crea la barra menú con sus opciones
        toolbar = Menu(self.root)
        self.root["menu"] = toolbar

        self.menu_opciones = Menu(toolbar)
        self.menu_ayuda = Menu(toolbar)
        toolbar.add_cascade(menu=self.menu_opciones, label="Acciones")
        toolbar.add_cascade(menu=self.menu_ayuda, label="Ayuda")
                 
        self.menu_opciones.add_command(label="Registrar alumno", 
                               command=self.top_student.show)

        tabController = Notebook(self.root)
        tabController.grid(column=0, row=0)

        self.studentsFrame = Frame(tabController, padding=(10,10))
        tabController.add(self.studentsFrame, text="Alumnos")

        self.teachersFrame = Frame(tabController, padding=(10,10))
        tabController.add(self.teachersFrame, text="Docentes")

        self.coursesFrame = Frame(tabController, padding=(10,10))
        tabController.add(self.coursesFrame, text="Cursos")

        self.create_frame_students()

    def create_frame_students(self):
        self.tableStudentsFrame = Frame(self.studentsFrame, relief="groove", padding=(5,5))
        self.tableStudentsFrame.grid(column=15, row=0, padx=10)

        students = self.cursor.execute("select * from Cursante")
        table = Table(self.tableStudentsFrame, students.fetchall())

        self.fieldsFrame = Frame(self.studentsFrame, relief="groove", padding=(15,15))
        self.fieldsFrame.grid(column=0, row=0, padx=10, pady=10)

        lbl_newStudent = Label(self.fieldsFrame, text="Formulario de registro")
        lbl_newStudent.grid(row=0, column=0, columnspan=18, pady=(5,10))

        lbl_dni = Label(self.fieldsFrame, text="DNI: ", width=10)
        lbl_dni.grid(row=1, column=0, columnspan=10)

        self.dni = Entry(self.fieldsFrame, width=40)
        self.dni.grid(row=2, column=0, columnspan=40, pady=(0,15))

        lbl_name = Label(self.fieldsFrame, text="Nombre: ", width=10)
        lbl_name.grid(row=3, column=0, columnspan=10)

        self.name = Entry(self.fieldsFrame, width=40)
        self.name.grid(row=4, column=0, columnspan=40, pady=(0,15))

        lbl_surname = Label(self.fieldsFrame, text="Apellido: ", width=10)
        lbl_surname.grid(row=5, column=0, columnspan=10)

        self.surname = Entry(self.fieldsFrame, width=40)
        self.surname.grid(row=6, column=0, columnspan=40, pady=(0,15))

        lbl_email = Label(self.fieldsFrame, text="Email: ", width=10)
        lbl_email.grid(row=7, column=0, columnspan=10)

        self.email = Entry(self.fieldsFrame, width=40)
        self.email.grid(row=8, column=0, columnspan=40, pady=(0,15))

        lbl_phone = Label(self.fieldsFrame, text="Teléfono: ", width=10)
        lbl_phone.grid(row=9, column=0, columnspan=10)

        self.phone = Entry(self.fieldsFrame, width=40)
        self.phone.grid(row=10, column=0, columnspan=40, pady=(0,15))

        lbl_institute = Label(self.fieldsFrame, text="Institución: ", width=10)
        lbl_institute.grid(row=11, column=0, columnspan=10)

        self.institute = Entry(self.fieldsFrame, width=40)
        self.institute.grid(row=12, column=0, columnspan=40, pady=(0,15))

        self.btn_createStudent = Button(self.fieldsFrame, text="Registrar")
        self.btn_createStudent.grid(row=13, column=0, columnspan=40, pady=5)


class WinLogin(Tk):

    def __init__(self, connection, *args, **kwargs):
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
    try:
        connection = sqlite3.connect("./Database.db")
    except Exception as e:
        messagebox.showerror("Error de base de datos", e)

    """ win_login = WinLogin(connection)
    
    if win_login.accepted: """
    app = MainApplication(connection)
