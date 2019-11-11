from tkinter import messagebox as mb, StringVar, Toplevel
from tkinter.ttk import Frame, Label, Entry, Button
from Form import Form
import sqlite3

class Course:

    connection = None
    modified = False

    def create(self, data):
        cur = Course.connection.cursor()
        sql = """INSERT INTO `Curso` VALUES 
                  (NULL, ?, ?, ?, ?, ?)"""

        try:
            cur.execute(sql, data)
            Course.connection.commit()
            self.need_update()
            mb.showinfo("Información", "El registro se ha creado con éxito!")

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)

    def delete(self, id_register):
        if mb.askyesnocancel("Confimación", "Está seguro que desea eliminar \nlos datos del curso?"):
            cur = Course.connection.cursor()
            sql = """DELETE FROM `Curso` 
                     WHERE codigo = ?"""
            
            try:
                cur.execute(sql, (id_register,))
                Course.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha eliminado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    def update(self, id_register, data):
        if mb.askyesnocancel("Confimación", "Está seguro que desea modificar \nlos datos del curso?"):
            cur = Course.connection.cursor()
            data.append(id_register)

            sql = """UPDATE `Curso` 
                     SET nombre = ?, fecha_inicio = ?, fecha_fin = ?, carga_horaria = ?, lugar_dictado = ?
                     WHERE codigo = ?"""

            try:
                cur.execute(sql, data)
                Course.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha modificado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    def get_all(self):
        cur = Course.connection.cursor()
        sql = """SELECT * FROM `Curso`"""

        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)        

    def get_register(self, id_register):
        cur = Course.connection.cursor()
        sql = """SELECT * FROM `Curso` WHERE codigo = ?"""

        try:
            cur.execute(sql, (id_register,))
            return cur.fetchone()

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)       

    @classmethod
    def need_update(self):
        CourseForm.modified = True

    @classmethod
    def is_update(self):
        return CourseForm.modified
    
    @classmethod
    def updated(self):
        CourseForm.modified = False


class CourseForm(Course, Form):
    
    def __init__(self, form_type):
        Course.__init__(self)
        
        # Al momento de crear la ventana, también la oculta
        self.root = Toplevel()
        self.root.withdraw()
        self.root.title("Crear curso" if (form_type == "create") else "Detalles del Curso")
        self.root.resizable(0,0)

        # Al cerrar la ventana, esta sólo se ocultará.
        # Esto evita crearla cada vez que se la necesita.
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

        fieldsFrame = Frame(self.root, relief="groove", padding=(15,15))
        fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        lbl_name = Label(fieldsFrame, text="Nombre: ", width=10)
        lbl_name.grid(row=1, column=0, columnspan=10)

        name = StringVar()
        e_name = Entry(fieldsFrame, textvariable=name, width=40)
        e_name.grid(row=2, column=0, columnspan=40, pady=(0,15))

        lbl_date_start = Label(fieldsFrame, text="Fecha de inicio: ", width=15)
        lbl_date_start.grid(row=3, column=0, columnspan=15)

        date_start = StringVar()
        e_date_start = Entry(fieldsFrame, textvariable=date_start, width=40)
        e_date_start.grid(row=4, column=0, columnspan=40, pady=(0,15))

        lbl_date_end = Label(fieldsFrame, text="Fecha de fin: ", width=15)
        lbl_date_end.grid(row=5, column=0, columnspan=15)

        date_end = StringVar()
        e_date_end = Entry(fieldsFrame, textvariable=date_end, width=40)
        e_date_end.grid(row=6, column=0, columnspan=40, pady=(0,15))

        lbl_workload = Label(fieldsFrame, text="Carga horaria: ", width=15)
        lbl_workload.grid(row=7, column=0, columnspan=15)

        workload = StringVar()
        e_workload = Entry(fieldsFrame, textvariable=workload, width=40)
        e_workload.grid(row=8, column=0, columnspan=40, pady=(0,15))

        lbl_place = Label(fieldsFrame, text="Lugar: ", width=10)
        lbl_place.grid(row=9, column=0, columnspan=10)

        place = StringVar()
        e_place = Entry(fieldsFrame, textvariable=place, width=40)
        e_place.grid(row=10, column=0, columnspan=40, pady=(0,15))

        Form.__init__(self, {"nombre":name, "fecha_inicio":date_start, "fecha_fin":date_end,
                             "carga_horaria":workload, "lugar_dictado":place})

        name.trace("w", lambda *args: self.validate_str(name, *args))
        date_start.trace("w", lambda *args: self.validate_date(date_start, *args))
        date_end.trace("w", lambda *args: self.validate_date(date_end, *args))
        workload.trace("w", lambda *args: self.validate_int(workload, *args))
        place.trace("w", lambda *args: self.validate_str(place, *args))

        if form_type == "details":
            btn_modify = Button(fieldsFrame, text="Modificar",
                                command=lambda r_id=self.id_register, data=self.get_data(): self.update(r_id, data))
            btn_modify.grid(row=11, column=0, columnspan=20, pady=5)

            btn_delete = Button(fieldsFrame, text="Eliminar",
                                command=self.delete)
            btn_delete.grid(row=11, column=20, columnspan=20, pady=5)

        elif form_type == "create":
            lbl_newStudent = Label(fieldsFrame, text="Formulario de registro")
            lbl_newStudent.grid(row=0, column=0, columnspan=18, pady=(5,10))

            btn_createStudent = Button(fieldsFrame, text="Registrar",
                                            command=self.create)
            btn_createStudent.grid(row=11, column=0, columnspan=40, pady=(5,40))

    def show(self, id_register):
        self.id_register = id_register
        register = self.get_register(id_register)

        # Se limpian los campos y se carga la nueva
        # info, mediante el llamado a la clase padre 'Form'
        self.clean_fields()
        self.load_data(register)

        # Se muestra la ventana
        self.root.deiconify()

    def hide(self):
        # Se oculta la ventana
        self.root.withdraw()
