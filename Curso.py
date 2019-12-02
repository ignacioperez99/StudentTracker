from tkinter import messagebox as mb, StringVar, Toplevel, Listbox
from tkinter.ttk import Frame, Label, Entry, Button
from Form import Form
from Calendar import DatePicker
import sqlite3
from dateutil import parser, rrule as drrule
from datetime import date

class Curso:

    connection = None
    modified = False

    def create(self, data):
        '''
        Crea un nuevo registro.
        '''
        
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

    def delete(self, id_register):
        '''
        Elimina un registro en particular.
        '''
        
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

    def update(self, id_register, data):
        '''
        Actualiza la información de un registro en particular.
        '''
        
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

    def add_cursante(self, data):
        '''
        Inscribe un alumno a un curso
        '''
        
        cur = Curso.connection.cursor()
        sql = """INSERT INTO `Inscripto` VALUES 
                  (NULL, NULL, NULL, ?, ?, ?)"""

        try:
            cur.execute(sql, data)
            Curso.connection.commit()
            self.need_update()
            mb.showinfo("Información", "Se incribió correctamente al alumno!")

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)

    def remove_cursante(self, id_register, id_curso):
        '''
        Elimina la incripción de un alumno a un curso
        '''
        
        if mb.askyesnocancel("Confimación", "Está seguro que desea remover \nla incripción del alumno?"):
            cur = Curso.connection.cursor()
            sql = """DELETE FROM `Inscripto`
                     WHERE cursante = ? AND curso = ?"""

            try:
                cur.execute(sql, (id_register, id_curso))
                Curso.connection.commit()
                self.need_update()

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    def add_docente(self, id_register, id_curso):
        '''
        Vincula a un docente con un curso.
        '''
        
        cur = Curso.connection.cursor()
        sql = """INSERT INTO `DocenteCurso` VALUES (?, ?)"""

        try:
            cur.execute(sql, (id_register, id_curso))
            Curso.connection.commit()
            self.need_update()

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)

    def remove_docente(self, id_register, id_curso):
        '''
        Elimina el vínculo entre un docente y un curso.
        '''
        
        if mb.askyesnocancel("Confimación", "Está seguro que desea remover \nal docente del curso?"):
            cur = Curso.connection.cursor()
            sql = """DELETE FROM `DocenteCurso`
                    WHERE docente = ? AND curso = ?"""

            try:
                cur.execute(sql, (id_register, id_curso))
                Curso.connection.commit()
                self.need_update()

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    @classmethod
    def get_all(self):
        '''
        Retorna todos los registros existentes.
        '''
        
        cur = Curso.connection.cursor()
        sql = """SELECT * FROM `Curso`"""

        try:
            cur.execute(sql)
            return {"names": [ desc[0] for desc in cur.description], 
                    "data":  cur.fetchall()}
        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)        

    @classmethod
    def get_register(self, id_register):
        '''
        Retorna un registro en particular.
        '''
        
        cur = Curso.connection.cursor()
        sql = """SELECT * FROM `Curso` WHERE codigo = ?"""

        try:
            cur.execute(sql, (id_register,))
            return cur.fetchone()

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)       

    @classmethod
    def get_miembros(self, id_curso):
        '''
        Retorna un diccionario con los inscriptos y docentes
        que están vinculados con un curso en particular.
        '''
        
        cur = Curso.connection.cursor()
        sql_cursantes = """SELECT C.codigo, C.nombre, C.apellido 
                           FROM `Inscripto` as I INNER JOIN `Cursante` as C ON I.cursante=C.codigo
                           WHERE I.curso = ?"""
        sql_docentes = """SELECT D.codigo, D.nombre, D.apellido 
                          FROM `Docente` as D, `Curso` as C, `DocenteCurso` as DC
                          WHERE DC.curso = ?"""

        try:
            cursantes= cur.execute(sql_cursantes, (id_curso,)).fetchall()
            docentes= cur.execute(sql_docentes, (id_curso,)).fetchall()
            
            return {"cursantes": {"names": [ desc[0] for desc in cur.description], 
                                  "data":  cursantes}, 
                    "docentes":  {"names": [ desc[0] for desc in cur.description], 
                                  "data":  docentes}}

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e) 

    @classmethod
    def get_no_miembros(self, id_curso):
        '''
        Retorna los alumnos y docentes que no pertenecen a
        un curso en particular.
        '''
        
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
                                 "data":  cursantes}, 
                    "docentes": {"names": [ desc[0] for desc in cur.description], 
                                 "data":  docentes}}

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e) 

    @classmethod
    def get_dates(self, id_curso):
        '''
        Retorna la cantidad de días entre 
        '''
        
        def parse_date(fecha):
            if type(fecha) == str:
                fecha = parser.parse(fecha)

            return date(fecha.year,fecha.month,fecha.day)

        cur = Curso.connection.cursor()
        sql_curso = """SELECT fecha_inicio, fecha_fin 
                       FROM `Curso`
                       WHERE codigo = ?"""
        dates_curso = cur.execute(sql_curso, (id_curso,)).fetchone()

        start = parse_date(dates_curso[0])
        end = parse_date(dates_curso[1])
        cant = abs(start-end).days
        """ days=list(map(parse_date,drrule.rrule(drrule.DAILY, dtstart=start, until=end))) """
        print(f"start: {start}\nend: {end}\ndays: {cant}")


    @classmethod
    def need_update(self):
        '''
        Deja constancia de que la información contenida en la tabla
        fue modificada y necesita ser actualizada visualmente.
        '''
        Curso.modified = True

    @classmethod
    def is_update(self):
        '''
        Retorna verdadero si la tabla necesita ser actualizada visualmente.
        '''
        return Curso.modified
    
    @classmethod
    def updated(self):
        '''
        Deja constancia de que la tabla fue actualizada visualmente.
        '''
        Curso.modified = False


class FormInscriptos(Curso, Form):

    def __init__(self, form_type):
        Curso.__init__(self)
        Form.__init__(self)

        self.id_curso = None
        self.form_type = form_type

        fieldsFrame = Frame(self.root, padding=10)
        fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        lbl_alumnos = Label(fieldsFrame, width=30)
        lbl_alumnos.grid(row=2, column=0, columnspan=30)

        self.listaPersonas = Listbox(fieldsFrame, selectmode="extended", height=25, width=40)
        self.listaPersonas.grid(row=3, column=0, columnspan=40, pady=(5,10))

        btn_aceptar = Button(fieldsFrame, text="Aceptar", width=16)
        btn_aceptar.grid(row=4, column=0, columnspan=16)
        
        btn_cancelar = Button(fieldsFrame, text="Cancelar", width=16,
                              command=self.hide)
        btn_cancelar.grid(row=4, column=26, columnspan=16)

        if form_type == "add":
            self.set_title("Inscribir alumnos")
            lbl_alumnos.config(text="Seleccione los alumnos:")

            lbl_date = Label(fieldsFrame, text="Seleccione la fecha:", width=20)
            lbl_date.grid(row=0, column=0, columnspan=20)

            self.date = StringVar()
            e_date = Entry(fieldsFrame, textvariable=self.date, width=30)
            e_date.grid(row=1, column=0, columnspan=30, pady=(0,10))
            e_date.config(state="readonly")

            btn_date = Button(fieldsFrame, text="...", width=8,
                            command=lambda: self.date.set(DatePicker(fieldsFrame).selection()))
            btn_date.grid(row=1, column=32, columnspan=8, pady=(0,10))

            btn_aceptar.config(command=lambda: self.add_cursante())

        elif form_type == "remove":
            self.set_title("Remover inscriptos")
            lbl_alumnos.config(text="Seleccione los inscriptos:")
            btn_aceptar.config(command=lambda: self.remove_cursante())

    def add_cursante(self):
        fecha = self.date.get()
        curso = self.id_curso
        alumnos = [self.listaPersonas.get(index) for index in self.listaPersonas.curselection()]
        
        for alumno in alumnos:
            super().add_cursante((fecha, alumno.strip().split()[0], curso))

        self.hide()

    def remove_cursante(self):
        curso = self.id_curso
        alumnos = [self.listaPersonas.get(index) for index in self.listaPersonas.curselection()]

        for alumno in alumnos:
            super().remove_cursante(alumno.strip().split()[0], curso)

        self.hide()

    def get_all(self):
        if self.form_type == "add":
            return self.get_no_miembros(self.id_curso)["cursantes"]

        elif self.form_type == "remove":
            return self.get_miembros(self.id_curso)["cursantes"]

    def show(self, id_curso):
        self.id_curso = id_curso

        data = self.get_all()["data"]
        
        for row in list(data):
            iD, name = row[0], f"{row[1]}, {row[2]}".upper()
            self.listaPersonas.insert("end", "   {:>4d}       {:<40s}".format(iD, name))

        super().show()

    def hide(self):
        self.date.set("")
        self.listaPersonas.delete(0, 'end')

        super().hide()


class FormAsistencias(Curso, Form):

    def __init__(self):
        Curso.__init__(self)
        Form.__init__(self)

        self.id_curso = None
        self.set_title("Asistencias")

        fieldsFrame = Frame(self.root, padding=10)
        fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        lbl_date = Label(fieldsFrame, text="Seleccione la fecha:", width=20)
        lbl_date.grid(row=0, column=0, columnspan=20)

        date = StringVar()
        e_date = Entry(fieldsFrame, textvariable=date, width=30)
        e_date.grid(row=1, column=0, columnspan=30)
        e_date.config(state="readonly")

        btn_date = Button(fieldsFrame, text="...", width=8,
                           command=lambda: date.set(DatePicker(fieldsFrame).selection()))
        btn_date.grid(row=1, column=32, columnspan=8)

        lbl_inscriptos = Label(fieldsFrame, text="Seleccione los inscriptos:", width=30)
        lbl_inscriptos.grid(row=2, column=0, columnspan=30, pady=(10,5))

        self.listaPersonas = Listbox(fieldsFrame, highlightthickness=0, selectmode="extended", 
                                     height=25, width=40)
        self.listaPersonas.grid(row=3, column=0, columnspan=40, pady=(0,10))

        """ self.listbox.insert(0, "Python", "C", "C++", "Java")
        self.listbox.itemconfigure(0, bg="#00aa00", fg="#fff")
        self.listbox.itemconfigure(3, bg="#ff0000", fg="#fff") """

        btn_aceptar = Button(fieldsFrame, text="Aceptar", width=16)
        btn_aceptar.grid(row=4, column=0, columnspan=16)
        
        btn_cancelar = Button(fieldsFrame, text="Cancelar", width=16,
                              command=self.hide)
        btn_cancelar.grid(row=4, column=26, columnspan=16)

    def get_all(self):
        return self.get_miembros(self.id_curso)["cursantes"]

    def show(self, id_curso):
        self.id_curso = id_curso

        data = self.get_miembros(self.id_curso)["cursantes"]["data"]
        
        for row in list(data):
            iD, name = row[0], f"{row[1]}, {row[2]}".upper()
            self.listaPersonas.insert("end", "   {:>4d}       {:<40s}".format(iD, name))

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
        fieldsFrame.grid(row=0, column=0, padx=10, pady=(0,10))

        lbl_select = Label(fieldsFrame, text="Seleccione los docentes:", width=26)
        lbl_select.grid(row=0, column=0, columnspan=26)

        self.listaPersonas = Listbox(fieldsFrame, highlightthickness=0, selectmode="extended", 
                                     height=25, width=40)
        self.listaPersonas.grid(row=1, column=0, columnspan=40, pady=(5,10))

        btn_aceptar = Button(fieldsFrame, text="Aceptar", width=16)
        btn_aceptar.grid(row=2, column=0, columnspan=16)

        btn_cancelar = Button(fieldsFrame, text="Cancelar", width=16,
                              command=self.hide)
        btn_cancelar.grid(row=2, column=24, columnspan=16)

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
        
        for row in list(data): 
            iD, name = row[0], f"{row[1]}, {row[2]}".upper()
            self.listaPersonas.insert("end", "   {:>4d}       {:<40s}".format(iD, name))

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
