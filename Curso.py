from tkinter import messagebox as mb, StringVar, Toplevel, Listbox
from tkinter.ttk import Frame, Label, Entry, Button, Combobox
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
        if data[0] and data[1] and data[2] and data[3] and data[4]:
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

        else:
            mb.showwarning("Advertencia!", "Todos los campos son obligatorios.")

    def delete(self, id_register):
        '''
        Elimina un registro en particular.
        '''
        
        if mb.askyesnocancel("Confimación", "Está seguro que desea eliminar \nlos datos del curso?"):
            cur = Curso.connection.cursor()
            sql = """DELETE FROM `Curso` 
                     WHERE codigo = ?"""

            sql_insc = """DELETE FROM `Inscripto` 
                          WHERE curso = ?"""

            sql_dc = """DELETE FROM `DocenteCurso` 
                        WHERE curso = ?"""

            sql_asist = """DELETE FROM `Asistencia` 
                           WHERE curso = ?"""
            
            try:
                cur.execute(sql, (id_register,))
                cur.execute(sql_insc, (id_register,))
                cur.execute(sql_dc, (id_register,))
                cur.execute(sql_asist, (id_register,))
                Curso.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha eliminado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    def update(self, id_register, data):
        '''
        Actualiza la información de un registro en particular.
        '''

        if data[0] and data[1] and data[2] and data[3] and data[4]:
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
            
        else:
            mb.showwarning("Advertencia!", "Todos los campos son obligatorios.")

    def add_cursante(self, insc_date, id_register, id_curso):
        '''
        Inscribe un alumno a un curso
        '''

        cur = Curso.connection.cursor()
        dates = self.get_dates(id_curso)
        sql = """INSERT INTO `Inscripto` VALUES 
                 (NULL, NULL, NULL, ?, ?, ?)"""

        try:
            cur.execute(sql, (insc_date, id_register, id_curso))

            for date in dates:
                sql_asist = '''INSERT INTO `Asistencia` VALUES
                                (NULL, ?, ?, (SELECT codigo
                                                  FROM `Inscripto`
                                                  WHERE fecha_inscripcion = ? AND 
                                                        cursante = ? AND 
                                                        curso = ?), ?)'''
                cur.execute(sql_asist, (date, False, insc_date, id_register, id_curso, id_curso))

            Curso.connection.commit()
            self.need_update()
            """ mb.showinfo("Información", "Se incribió correctamente al alumno!") """

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)

    def remove_cursante(self, id_register):
        '''
        Elimina la incripción de un alumno a un curso y a su vez
        todos los datos vinculados a su asistencia
        '''

        cur = Curso.connection.cursor()
        sql = """DELETE FROM `Inscripto`
                    WHERE codigo = ?"""

        sql_asist = """DELETE FROM `Asistencia`
                        WHERE inscripto = ?"""

        try:
            cur.execute(sql, (id_register,))
            cur.execute(sql_asist, (id_register,))
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

        cur = Curso.connection.cursor()
        sql = """DELETE FROM `DocenteCurso`
                WHERE docente = ? AND curso = ?"""

        try:
            cur.execute(sql, (id_register, id_curso))
            Curso.connection.commit()
            self.need_update()

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)

    def update_asistencia(self, date, id_register, id_curso, state):
        cur = Curso.connection.cursor()
        sql = '''UPDATE `Asistencia` 
                 SET asistio = ?
                 WHERE fecha = ? AND
                       curso = ? AND
                       inscripto = ?'''

        try:
            cur.execute(sql, (state, date, id_curso, id_register))
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
        sql_cursantes = """SELECT I.codigo, C.nombre, C.apellido, I.fecha_inscripcion
                           FROM `Inscripto` as I INNER JOIN `Cursante` as C ON I.cursante=C.codigo
                           WHERE I.curso = ?"""
        sql_docentes = """SELECT D.codigo, D.nombre, D.apellido 
                          FROM `Docente` as D INNER JOIN `DocenteCurso` as DC ON DC.docente = D.codigo 
                                              INNER JOIN `Curso` as C ON DC.curso = C.codigo
                          WHERE DC.curso = ?"""
        try:
            c_data = cur.execute(sql_cursantes, (id_curso,)).fetchall()
            cursantes = {"names": [ desc[0] for desc in cur.description], 
                         "data":  c_data}

            d_data = cur.execute(sql_docentes, (id_curso,)).fetchall()
            docentes = {"names": [ desc[0] for desc in cur.description], 
                        "data":  d_data}

            return {"cursantes": cursantes, "docentes":  docentes}

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e) 

    @classmethod
    def get_no_miembros(self, id_curso):
        '''
        Retorna los alumnos y docentes que no pertenecen a
        un curso en particular.
        '''

        cur = Curso.connection.cursor()
        sql_cursantes = """SELECT C.codigo, C.nombre, C.apellido 
                           FROM `Cursante` as C
                           WHERE C.codigo NOT IN (
                                SELECT I.cursante
                                FROM `Inscripto` as I
                                WHERE I.curso = ?
                           )"""
        sql_docentes = """SELECT D.codigo, D.nombre, D.apellido
                          FROM `Docente` as D
                          WHERE D.codigo NOT IN (
                                SELECT DC.docente
                                FROM `DocenteCurso` as DC
                                WHERE DC.curso = ?
                          )"""

        try:
            c_data= cur.execute(sql_cursantes, (id_curso,)).fetchall()
            cursantes = {"names": [desc[0] for desc in cur.description], 
                         "data":  c_data}
            
            d_data= cur.execute(sql_docentes, (id_curso,)).fetchall()
            docentes = {"names": [desc[0] for desc in cur.description], 
                        "data":  d_data}
            
            return {"cursantes": cursantes, "docentes": docentes}

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e) 

    @classmethod
    def get_dates(self, id_curso):
        '''
        Retorna un arreglo con los días 
        entre la fecha de inicio y la de fin.
        '''
        # Convierte las fechas string y datetime en
        # formato date del tipo AAAA/MM/DD
        def parse_date(fecha):
            if type(fecha) == str:
                fecha = parser.parse(fecha)

            return date(fecha.year,fecha.month,fecha.day)

        cur = Curso.connection.cursor()
        sql_curso = """SELECT fecha_inicio, fecha_fin 
                       FROM `Curso`
                       WHERE codigo = ?"""
        dates_curso = cur.execute(sql_curso, (id_curso,)).fetchone()

        start = parse_date(dates_curso[0]) if dates_curso else None
        end = parse_date(dates_curso[1]) if dates_curso else None

        return list(map(parse_date,drrule.rrule(drrule.DAILY, dtstart=start, until=end)))
    
    @classmethod
    def get_asistencias(self, id_curso):
        '''
        Retorna los alumnos y docentes que no pertenecen a
        un curso en particular.
        '''

        dates = self.get_dates(id_curso)
        sql_dates = ""
        

        for date in dates:
            sql_dates = (sql_dates + 
                         f""", (SELECT CASE 
                                        WHEN asistio = 1 
                                        THEN 'Asistió' 
                                        ELSE '---' 
                                     END 
                              FROM Asistencia 
                              WHERE fecha = '{str(date)}' AND 
                                    inscripto = I.codigo) as '{str(date)}'""")

        cur = Curso.connection.cursor()
        sql = f'''SELECT I.codigo || ", " || C.nombre || ", " || C.apellido as Inscripto{sql_dates}
                  FROM Asistencia as A INNER JOIN Inscripto as I ON A.inscripto = I.codigo
                                       INNER JOIN Cursante  as C ON I.cursante = C.codigo
                  WHERE A.curso = ?
                  GROUP BY A.inscripto, C.nombre, C.apellido'''

        a_data = cur.execute(sql, (id_curso,)).fetchall()
        
        return {"names": [desc[0] for desc in cur.description], 
                "data": a_data}

    @classmethod
    def get_data_certificados(self, id_curso):
        cur = Curso.connection.cursor()
        sql_asist = """SELECT I.codigo, C.dni, C.nombre || ' ' || C.apellido as nombre
                       FROM Inscripto as I INNER JOIN Cursante as C ON I.cursante = C.codigo
                       WHERE I.curso = ? AND 
                             0 NOT IN (SELECT asistio
                                       FROM Asistencia
                                       WHERE inscripto = I.codigo AND
                                             curso = I.curso)"""

        sql_docs = """SELECT D.nombre || ' ' || D.apellido as nombre
                      FROM Docente as D INNER JOIN DocenteCurso as DC ON DC.docente = D.codigo
                                        INNER JOIN Curso as C ON DC.curso = C.codigo
                      WHERE DC.curso = ?"""  
        
        sql_cur = """SELECT nombre
                     FROM Curso
                     WHERE codigo = ?"""

        dates = sorted(self.get_dates(id_curso))
        dict_dates = {}
        for date in dates:
            dict_dates.setdefault(date.year, {}).setdefault(date.month, []).append(date.day)
         
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        str_date = ""
        for i, year in enumerate(dict_dates.keys()):
            for j, month in enumerate(dict_dates[year].keys()):
                for k, day in enumerate(dict_dates[year][month]):
                    str_date = (str_date + str(day) + (" y " if k == len(dict_dates[year][month])-2 else
                                                       (", " if k < len(dict_dates[year][month])-1 else "")))

                str_date = (str_date + " de " + meses[int(month)-1] + 
                            (" y " if j == len(dict_dates[year].keys())-2 else
                             (", " if j < len(dict_dates[year].keys())-1 else "")))

            str_date = (str_date + " de " + str(year) + (" y " if i == len(dict_dates.keys())-2 else
                                                         (", " if i < len(dict_dates.keys())-1 else "")))

        asistieron = [dict(item) for item in cur.execute(sql_asist, (id_curso,)).fetchall()]
        docentes = [dict(item)["nombre"] for item in cur.execute(sql_docs, (id_curso,)).fetchall()]
        curso = cur.execute(sql_cur, (id_curso,)).fetchone()

        str_docentes = ""
        for i, docente in enumerate(docentes):
            str_docentes = (str_docentes + str(docente) + (" y " if i == len(docentes)-2 else
                                                           (", " if i < len(docentes)-1 else "")))

        return {"asistieron": [dict(item) for item in asistieron],
                "docentes": str_docentes,
                "fechas": str_date,
                "curso": dict(curso)["nombre"]}

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

        self.listaPersonas = Listbox(fieldsFrame, highlightthickness=0, selectmode="extended", 
                                     height=25, width=40)
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
        
        if fecha and alumnos:
            for alumno in alumnos:
                super().add_cursante(fecha, alumno.strip().split()[0], curso)

            self.hide()

        else:
            mb.showwarning("Advertencia!", "Por favor, seleccione la fecha y los\nalumnos a inscribir.") 

    def remove_cursante(self):
        '''
        Elimina a los incriptos seleccionados de un curso.
        '''
        alumnos = [self.listaPersonas.get(index) for index in self.listaPersonas.curselection()]

        if alumnos:
            if mb.askyesnocancel("Confimación", "Está seguro que desea remover \nlos inscriptos seleccionados del curso?"):

                for alumno in alumnos:
                    super().remove_cursante(alumno.strip().split()[0])

                self.hide()
        
        else:
            mb.showwarning("Advertencia!", "Por favor, seleccione los inscriptos a remover.") 

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
        if self.form_type == "add":
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

        self.date = StringVar()
        self.cb_date = Combobox(fieldsFrame, textvariable=self.date, width=36,
                                state="readonly")
        self.cb_date.grid(row=1, column=0, columnspan=36, pady=(5,10))

        lbl_inscriptos = Label(fieldsFrame, text="Seleccione los inscriptos que asistieron:", width=40)
        lbl_inscriptos.grid(row=2, column=0, columnspan=40)

        self.listaPersonas = Listbox(fieldsFrame, highlightthickness=0, selectmode="extended", 
                                     height=25, width=40)
        self.listaPersonas.grid(row=3, column=0, columnspan=40, pady=(5,10))

        btn_aceptar = Button(fieldsFrame, text="Aceptar", width=16,
                             command=lambda: self.update_asistencia())
        btn_aceptar.grid(row=4, column=0, columnspan=16)
        
        btn_cancelar = Button(fieldsFrame, text="Cancelar", width=16,
                              command=self.hide)
        btn_cancelar.grid(row=4, column=26, columnspan=16)

    def update_asistencia(self):
        asistieron = self.listaPersonas.curselection()
        inscriptos = [item.strip().split(" ")[0] for item in self.listaPersonas.get(0, 'end')]
        date = self.date.get()
        curso = self.id_curso

        for index, inscripto in enumerate(inscriptos):
            super().update_asistencia(date, inscripto, curso, (True if index in asistieron else False))

        self.hide()

    def get_all(self):
        return self.get_asistencias(self.id_curso)

    def show(self, id_curso):
        self.id_curso = id_curso

        values = self.get_dates(self.id_curso)
        self.cb_date.config(values=values)
        self.cb_date.current(0)

        data = self.get_miembros(self.id_curso)["cursantes"]["data"]
        
        for i, row in enumerate(list(data)):
            iD, name = row[0], f"{row[1]}, {row[2]}".upper()
            self.listaPersonas.insert(i, "   {:>4d}       {:<40s}".format(iD, name))

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
            btn_aceptar.config(command=lambda: self.add_docente())

        elif form_type == "remove":
            self.set_title("Eliminar docentes")
            btn_aceptar.config(command=lambda: self.remove_docente())

    def add_docente(self):
        curso = self.id_curso
        docentes = [self.listaPersonas.get(index) for index in self.listaPersonas.curselection()]
        
        for docente in docentes:
            super().add_docente(docente.strip().split()[0], curso)

        self.hide()

    def remove_docente(self):
        curso = self.id_curso
        docentes = [self.listaPersonas.get(index) for index in self.listaPersonas.curselection()]
        
        if mb.askyesnocancel("Confimación", "Está seguro que desea remover \na los docentes seleccionados del curso?"):

            for docente in docentes:
                super().remove_docente(docente.strip().split()[0], curso)

        self.hide()

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
        workload.trace("w", lambda *args: self.validate_int(workload, *args))
        place.trace("w", lambda *args: self.validate_place(place, *args))


class FormCreateCurso(FormCurso):

    def __init__(self):
        FormCurso.__init__(self)

        super().set_title("Crear curso")
        
        lbl_newStudent = Label(self.fieldsFrame, text="Formulario de registro")
        lbl_newStudent.grid(row=0, column=0, columnspan=18, pady=(5,10))

        btn_createStudent = Button(self.fieldsFrame, text="Registrar",
                                   command=lambda: (self.create(self.get_data()),
                                                    self.hide()))
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
                            command=lambda: (self.delete(self.id_register),
                                             self.hide()))
        btn_delete.grid(row=11, column=20, columnspan=20, pady=5)

    def show(self, id_register):
        self.id_register = id_register
        register = self.get_register(id_register)

        # Se limpian los campos y se carga la nueva
        # info, mediante el llamado a la clase padre 'Form'
        self.clean_fields()
        self.load_data(register)

        super().show()
