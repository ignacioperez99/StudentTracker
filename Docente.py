from tkinter import messagebox as mb, StringVar, Toplevel
from tkinter.ttk import Label, Entry, Button, Frame
from Form import Form
import sqlite3

class Docente:

    connection = None
    modified = False

    def create(self, data):
        if data[0] and data[1] and data[2] and data[5]:
            cur = Docente.connection.cursor()
            sql = """INSERT INTO `Docente` 
                    VALUES (NULL, ?, ?, ?, ?, ?, ?)"""

            try:
                cur.execute(sql, data)
                Docente.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha creado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)
        
        else:
            mb.showwarning("Advertencia!", "Los campos:\n   DNI, Nombre, Apellido y Título\nson obligatorios.")

    def delete(self, id_register):
        if mb.askyesnocancel("Confimación", "Está seguro que desea eliminar \nlos datos del docente?"):
            cur = Docente.connection.cursor()
            sql = """DELETE FROM `Docente` 
                     WHERE codigo = ?"""
            
            try:
                cur.execute(sql, (id_register,))
                Docente.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha eliminado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    def update(self, id_register, data):
        if data[0] and data[1] and data[2] and data[5]:
            if mb.askyesnocancel("Confimación", "Está seguro que desea modificar \nlos datos del docente?"):
                cur = Docente.connection.cursor()
                data.append(id_register)

                sql = """UPDATE `Docente` 
                         SET dni = ?, nombre = ?, apellido = ?, email = ?, telefono = ?, titulo = ? 
                         WHERE codigo = ?"""

                try:
                    cur.execute(sql, data)
                    Docente.connection.commit()
                    self.need_update()
                    mb.showinfo("Información", "El registro se ha modificado con éxito!")

                except Exception as e:
                    mb.showwarning("Ha ocurrido un problema", e)
        
        else:
            mb.showwarning("Advertencia!", "Los campos:\n   DNI, Nombre, Apellido y Título\nson obligatorios.")

    @classmethod
    def get_all(self):
        cur = Docente.connection.cursor()
        sql = """SELECT * FROM `Docente`"""

        try:
            cur.execute(sql)
            return {"names": [ desc[0] for desc in cur.description], "data":cur.fetchall()}

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)     

    @classmethod
    def get_register(self, id_register):
        cur = Docente.connection.cursor()
        sql = """SELECT * FROM `Docente` WHERE codigo = ?"""

        try:
            cur.execute(sql, (id_register,))
            return cur.fetchone()

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e) 

    @classmethod
    def need_update(self):
        Docente.modified = True

    @classmethod
    def is_update(self):
        return Docente.modified
    
    @classmethod
    def updated(self):
        Docente.modified = False


class FormDocente(Docente, Form):

    def __init__(self):
        Docente.__init__(self)

        Form.__init__(self)
    
        self.fieldsFrame = Frame(self.root, relief="groove", padding=(15,15))
        self.fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        lbl_dni = Label(self.fieldsFrame, text="DNI: ", width=10)
        lbl_dni.grid(row=1, column=0, columnspan=10)

        dni = StringVar() 
        e_dni = Entry(self.fieldsFrame, textvariable=dni, width=40)
        e_dni.grid(row=2, column=0, columnspan=40, pady=(0,15))

        lbl_name = Label(self.fieldsFrame, text="Nombre: ", width=10)
        lbl_name.grid(row=3, column=0, columnspan=10)

        name = StringVar()
        e_name = Entry(self.fieldsFrame, textvariable=name, width=40)
        e_name.grid(row=4, column=0, columnspan=40, pady=(0,15))

        lbl_surname = Label(self.fieldsFrame, text="Apellido: ", width=10)
        lbl_surname.grid(row=5, column=0, columnspan=10)

        surname = StringVar()
        e_surname = Entry(self.fieldsFrame, textvariable=surname, width=40)
        e_surname.grid(row=6, column=0, columnspan=40, pady=(0,15))

        lbl_email = Label(self.fieldsFrame, text="Email: ", width=10)
        lbl_email.grid(row=7, column=0, columnspan=10)

        email = StringVar()
        e_email = Entry(self.fieldsFrame, textvariable=email, width=40)
        e_email.grid(row=8, column=0, columnspan=40, pady=(0,15))

        lbl_phone = Label(self.fieldsFrame, text="Teléfono: ", width=10)
        lbl_phone.grid(row=9, column=0, columnspan=10)

        phone = StringVar()
        e_phone = Entry(self.fieldsFrame, textvariable=phone, width=40)
        e_phone.grid(row=10, column=0, columnspan=40, pady=(0,15))

        lbl_title = Label(self.fieldsFrame, text="Título: ", width=10)
        lbl_title.grid(row=11, column=0, columnspan=10)

        title = StringVar()
        e_title = Entry(self.fieldsFrame, textvariable=title, width=40)
        e_title.grid(row=12, column=0, columnspan=40, pady=(0,15))

        super().set_fields({"dni":dni, "nombre":name, "apellido":surname, 
                            "email":email, "telefono":phone, "titulo":title})

        dni.trace("w",     lambda *args: self.validate_dni(dni, *args))
        name.trace("w",    lambda *args: self.validate_str(name, *args))
        surname.trace("w", lambda *args: self.validate_str(surname, *args))
        phone.trace("w",   lambda *args: self.validate_phone(phone, *args))
        title.trace("w",   lambda *args: self.validate_str(title, *args))


class FormDetailsDocente(FormDocente):
    
    def __init__(self):
        FormDocente.__init__(self)
        
        super().set_title("Detalles del Docente")

        btn_modify = Button(self.fieldsFrame, text="Modificar",
                                command=lambda: self.update(self.id_register, self.get_data()))
        btn_modify.grid(row=13, column=0, columnspan=20, pady=5)

        btn_delete = Button(self.fieldsFrame, text="Eliminar",
                                command=lambda: self.delete(self.id_register))
        btn_delete.grid(row=13, column=20, columnspan=20, pady=5)

    def show(self, id_register):
        self.id_register = id_register
        register = self.get_register(id_register)

        # Se limpian los campos y se carga la nueva
        # info, mediante el llamado a la clase padre 'Form'
        self.clean_fields()
        self.load_data(register)

        super().show()

class FormCreateDocente(FormDocente):

    def __init__(self):
        FormDocente.__init__(self)

        super().set_title("Crear docente")
        
        lbl_newTeacher = Label(self.fieldsFrame, text="Formulario de registro")
        lbl_newTeacher.grid(row=0, column=0, columnspan=18, pady=(5,10))

        btn_createStudent = Button(self.fieldsFrame, text="Registrar",
                                        command=lambda: self.create(self.get_data()))
        btn_createStudent.grid(row=13, column=0, columnspan=40, pady=5)

    def show(self):
        # Se limpian los campos llamado a la clase padre 'Form'
        self.clean_fields()

        super().show()

