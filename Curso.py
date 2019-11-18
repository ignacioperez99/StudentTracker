from tkinter import messagebox as mb, StringVar, Toplevel, Listbox
from tkinter.ttk import Frame, Label, Entry, Button
from Form import Form
from Calendar import DatePicker
import sqlite3

class Curso:

    connection = None
    modified = False

    @classmethod
    def create(self, data):
        cur = Curso.connection.cursor()
        sql = """INSERT INTO `Curso` VALUES 
                  (NULL, ?, ?, ?, ?, ?)"""

        try:
            cur.execute(sql, data)
            Curso.connection.commit()
            self.need_update()
            mb.showinfo("Información", "El registro se ha creado con éxito!")

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)

    @classmethod
    def delete(self, id_register):
        if mb.askyesnocancel("Confimación", "Está seguro que desea eliminar \nlos datos del curso?"):
            cur = Curso.connection.cursor()
            sql = """DELETE FROM `Curso` 
                     WHERE codigo = ?"""
            
            try:
                cur.execute(sql, (id_register,))
                Curso.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha eliminado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    @classmethod
    def update(self, id_register, data):
        if mb.askyesnocancel("Confimación", "Está seguro que desea modificar \nlos datos del curso?"):
            cur = Curso.connection.cursor()
            data.append(id_register)

            sql = """UPDATE `Curso` 
                     SET nombre = ?, fecha_inicio = ?, fecha_fin = ?, carga_horaria = ?, lugar_dictado = ?
                     WHERE codigo = ?"""

            try:
                cur.execute(sql, data)
                Curso.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha modificado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    @classmethod
    def get_all(self):
        cur = Curso.connection.cursor()
        sql = """SELECT * FROM `Curso`"""

        try:
            cur.execute(sql)
            return {"names": [ desc[0] for desc in cur.description], "data":cur.fetchall()}
        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)        

    @classmethod
    def get_register(self, id_register):
        cur = Curso.connection.cursor()
        sql = """SELECT * FROM `Curso` WHERE codigo = ?"""

        try:
            cur.execute(sql, (id_register,))
            return cur.fetchone()

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)       

    @classmethod
    def get_miembros(self, id_curso):
        cur = Curso.connection.cursor()
        sql_cursantes = """SELECT C.codigo, C.nombre, C.apellido 
                           FROM `Inscripto` as I, `Cursante` as C
                           WHERE I.curso = ?"""
        sql_docentes = """SELECT D.codigo, D.nombre, D.apellido 
                          FROM `Docente` as D, `Curso` as C, `DocenteCurso` as DC
                          WHERE DC.curso = ?"""

        try:
            cursantes= cur.execute(sql_cursantes, (id_curso,)).fetchall()
            docentes= cur.execute(sql_docentes, (id_curso,)).fetchall()

            return {"cursantes": {"names": [ desc[0] for desc in cur.description], 
                                  "data":  (list(row) for row in cursantes)}, 
                    "docentes":  {"names": [ desc[0] for desc in cur.description], 
                                  "data":(list(row) for row in docentes)}}

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e) 

    @classmethod
    def get_no_miembros(self, id_curso):
        cur = Curso.connection.cursor()
        sql_cursantes = """SELECT DISTINCT C.codigo, C.nombre, C.apellido 
                           FROM `Cursante` as C
                           WHERE C.codigo NOT IN (
                                SELECT I.cursante
                                FROM `Inscripto` as I
                                WHERE I.curso = ?
                           )"""
        sql_docentes = """SELECT DISTINCT D.codigo, D.nombre, D.apellido
                          FROM `Docente` as D, `Curso` as C
                          WHERE D.codigo NOT IN (
                                SELECT DC.docente
                                FROM `DocenteCurso` as DC
                                WHERE DC.curso = ?
                          )"""

        try:
            cursantes= cur.execute(sql_cursantes, (id_curso,)).fetchall()
            docentes= cur.execute(sql_docentes, (id_curso,)).fetchall()
            
            return {"cursantes":{"names": [ desc[0] for desc in cur.description], 
                                  "data": (list(row) for row in cursantes)}, 
                    "docentes": {"names": [ desc[0] for desc in cur.description], 
                                 "data": (list(row) for row in docentes)}}

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e) 

    @classmethod
    def need_update(self):
        Curso.modified = True

    @classmethod
    def is_update(self):
        return Curso.modified
    
    @classmethod
    def updated(self):
        Curso.modified = False


class FormInscriptos(Curso, Form):

    def __init__(self, form_type):
        Curso.__init__(self)
        Form.__init__(self)

        self.id_curso = None
        self.form_type = form_type

        fieldsFrame = Frame(self.root, padding=10)
        fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        self.listaPersonas = Listbox(fieldsFrame, selectmode="extended", height=25, width=40)
        self.listaPersonas.grid(row=0, column=0, pady=(0,10))

        btn_aceptar = Button(fieldsFrame, text="Aceptar")
        btn_aceptar.grid(row=1, column=0)

        if form_type == "add":
            self.set_title("Inscribir alumnos")
            btn_aceptar.config(command=lambda: print("hola"))

        elif form_type == "remove":
            self.set_title("Eliminar alumnos")
            btn_aceptar.config(command=lambda: print("chau"))

    def get_all(self):
        if self.form_type == "add":
            return self.get_no_miembros(self.id_curso)["cursantes"]

        elif self.form_type == "remove":
            return self.get_miembros(self.id_curso)["cursantes"]

    def show(self, id_curso):
        self.id_curso = id_curso

        if self.form_type == "add":
            data = self.get_no_miembros(self.id_curso)["cursantes"]["data"]

        elif self.form_type == "remove":
            data = self.get_miembros(self.id_curso)["cursantes"]["data"]
        
        for row in data:
            self.listaPersonas.insert("end", row)

        super().show()

    def hide(self):
        self.listaPersonas.delete(0, 'end')

        super().hide()


class FormAsistencias(Curso, Form):

    def __init__(self, form_type):
        Curso.__init__(self)
        Form.__init__(self)

        self.id_curso = None
        self.form_type = form_type

        fieldsFrame = Frame(self.root, padding=10)
        fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        self.listaPersonas = Listbox(fieldsFrame, selectmode="extended", height=25, width=40)
        self.listaPersonas.grid(row=0, column=0, pady=(0,10))

        btn_aceptar = Button(fieldsFrame, text="Aceptar")
        btn_aceptar.grid(row=1, column=0)

        if form_type == "add":
            self.set_title("Inscribir alumnos")
            btn_aceptar.config(command=lambda: print("hola"))

        elif form_type == "remove":
            self.set_title("Eliminar alumnos")
            btn_aceptar.config(command=lambda: print("chau"))

    def get_all(self):
        if self.form_type == "add":
            return self.get_no_miembros(self.id_curso)["cursantes"]

        elif self.form_type == "remove":
            return self.get_miembros(self.id_curso)["cursantes"]

    def show(self, id_curso):
        self.id_curso = id_curso

        if self.form_type == "add":
            data = self.get_no_miembros(self.id_curso)["cursantes"]["data"]

        elif self.form_type == "remove":
            data = self.get_miembros(self.id_curso)["cursantes"]["data"]
        
        for row in data:
            self.listaPersonas.insert("end", row)

        super().show()

    def hide(self):
        self.listaPersonas.delete(0, 'end')

        super().hide()


class FormDocentesCurso(Curso, Form):

    def __init__(self, form_type):
        Curso.__init__(self)
        Form.__init__(self)

        self.id_curso = None
        self.form_type = form_type

        fieldsFrame = Frame(self.root, padding=10)
        fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        self.listaPersonas = Listbox(fieldsFrame, selectmode="extended", height=25, width=40)
        self.listaPersonas.grid(row=0, column=0, pady=(0,10))

        btn_aceptar = Button(fieldsFrame, text="Aceptar")
        btn_aceptar.grid(row=1, column=0)

        if form_type == "add":
            self.set_title("Agregar docentes")
            btn_aceptar.config(command=lambda: print("hola"))

        elif form_type == "remove":
            self.set_title("Eliminar docentes")
            btn_aceptar.config(command=lambda: print("chau"))

    def get_all(self):
        if self.form_type == "add":
            return self.get_no_miembros(self.id_curso)["docentes"]

        elif self.form_type == "remove":
            return self.get_miembros(self.id_curso)["docentes"]

    def show(self, id_curso):
        self.id_curso = id_curso

        if self.form_type == "add":
            data = self.get_no_miembros(self.id_curso)["docentes"]["data"]

        elif self.form_type == "remove":
            data = self.get_miembros(self.id_curso)["docentes"]["data"]
        
        for row in data:
            self.listaPersonas.insert("end", row)

        super().show()

    def hide(self):
        self.listaPersonas.delete(0, 'end')

        super().hide()


class FormCurso(Curso, Form):
    
    def __init__(self):
        Curso.__init__(self)
        Form.__init__(self)

        self.id_register = None

        self.fieldsFrame = Frame(self.root, relief="groove", padding=(15,15))
        self.fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        lbl_name = Label(self.fieldsFrame, text="Nombre: ", width=10)
        lbl_name.grid(row=1, column=0, columnspan=10)

        name = StringVar()
        e_name = Entry(self.fieldsFrame, textvariable=name, width=40)
        e_name.grid(row=2, column=0, columnspan=40, pady=(0,15))

        lbl_date_start = Label(self.fieldsFrame, text="Fecha de inicio: ", width=15)
        lbl_date_start.grid(row=3, column=0, columnspan=15)

        date_start = StringVar()
        e_date_start = Entry(self.fieldsFrame, textvariable=date_start, width=30)
        e_date_start.grid(row=4, column=0, columnspan=30, pady=(0,15))
        e_date_start.config(state="readonly")

        btn_start = Button(self.fieldsFrame, text="...", width=8,
                           command=lambda: date_start.set(DatePicker(self.fieldsFrame).selection()))
        btn_start.grid(row=4, column=30, columnspan=8, padx=(3,0), pady=(0,15))

        lbl_date_end = Label(self.fieldsFrame, text="Fecha de fin: ", width=15)
        lbl_date_end.grid(row=5, column=0, columnspan=15)

        date_end = StringVar()
        e_date_end = Entry(self.fieldsFrame, textvariable=date_end, width=30)
        e_date_end.grid(row=6, column=0, columnspan=30, pady=(0,15))
        e_date_end.config(state="readonly")

        btn_end = Button(self.fieldsFrame, text="...", width=8,
                           command=lambda: date_end.set(DatePicker(self.fieldsFrame).selection()))
        btn_end.grid(row=6, column=30, columnspan=8, padx=(3,0), pady=(0,15))

        lbl_workload = Label(self.fieldsFrame, text="Carga horaria: ", width=15)
        lbl_workload.grid(row=7, column=0, columnspan=15)

        workload = StringVar()
        e_workload = Entry(self.fieldsFrame, textvariable=workload, width=40)
        e_workload.grid(row=8, column=0, columnspan=40, pady=(0,15))

        lbl_place = Label(self.fieldsFrame, text="Lugar: ", width=10)
        lbl_place.grid(row=9, column=0, columnspan=10)

        place = StringVar()
        e_place = Entry(self.fieldsFrame, textvariable=place, width=40)
        e_place.grid(row=10, column=0, columnspan=40, pady=(0,15))

        super().set_fields({"nombre":name, "fecha_inicio":date_start, "fecha_fin":date_end,
                            "carga_horaria":workload, "lugar_dictado":place})

        name.trace("w", lambda *args: self.validate_str(name, *args))
        date_start.trace("w", lambda *args: self.validate_date(date_start, *args))
        date_end.trace("w", lambda *args: self.validate_date(date_end, *args))
        workload.trace("w", lambda *args: self.validate_int(workload, *args))
        place.trace("w", lambda *args: self.validate_place(place, *args))


class FormCreateCurso(FormCurso):

    def __init__(self):
        FormCurso.__init__(self)

        super().set_title("Crear curso")
        
        lbl_newStudent = Label(self.fieldsFrame, text="Formulario de registro")
        lbl_newStudent.grid(row=0, column=0, columnspan=18, pady=(5,10))

        btn_createStudent = Button(self.fieldsFrame, text="Registrar",
                                   command=lambda: self.create(self.get_data()))
        btn_createStudent.grid(row=11, column=0, columnspan=40, pady=(5,40))
    
    def show(self):
        # Se limpian los campos
        self.clean_fields()

        super().show()


class FormDetailsCurso(FormCurso):

    def __init__(self):
        FormCurso.__init__(self)

        super().set_title("Detalles del Curso")

        btn_modify = Button(self.fieldsFrame, text="Modificar",
                            command=lambda: self.update(self.id_register, self.get_data()))
        btn_modify.grid(row=11, column=0, columnspan=20, pady=5)

        btn_delete = Button(self.fieldsFrame, text="Eliminar",
                            command=lambda: self.delete(self.id_register))
        btn_delete.grid(row=11, column=20, columnspan=20, pady=5)

    def show(self, id_register):
        self.id_register = id_register
        register = self.get_register(id_register)

        # Se limpian los campos y se carga la nueva
        # info, mediante el llamado a la clase padre 'Form'
        self.clean_fields()
        self.load_data(register)

        super().show()
