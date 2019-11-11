from tkinter import messagebox as mb, StringVar, Toplevel
from tkinter.ttk import Frame, Label, Entry, Button, Combobox
from Form import Form
import sqlite3

class Cursante:

    connection = None
    modified = False

    def create(self, data):
        cur = Cursante.connection.cursor()
        sql = """INSERT INTO `Cursante` VALUES 
                  (NULL, ?, ?, ?, ?, ?, ?)"""

        try:
            cur.execute(sql, data)
            Cursante.connection.commit()
            self.need_update()
            mb.showinfo("Información", "El registro se ha creado con éxito!")

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)

    def delete(self, id_register):
        if mb.askyesnocancel("Confimación", "Está seguro que desea eliminar \nlos datos del alumno?"):
            cur = Cursante.connection.cursor()
            sql = """DELETE FROM `Cursante` 
                     WHERE codigo = ?"""
            
            try:
                cur.execute(sql, (id_register,))
                Cursante.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha eliminado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    def update(self, id_register, data):
        if mb.askyesnocancel("Confimación", "Está seguro que desea modificar \nlos datos del alumno?"):
            cur = Cursante.connection.cursor()
            data.append(id_register)
            sql = """UPDATE `Cursante` 
                     SET dni = ?, nombre = ?, apellido = ?, email = ?, telefono = ?, institucion = ? 
                     WHERE codigo = ?"""

            try:
                cur.execute(sql, data)
                Cursante.connection.commit()
                self.need_update()
                mb.showinfo("Información", "El registro se ha modificado con éxito!")

            except Exception as e:
                mb.showwarning("Ha ocurrido un problema", e)

    @classmethod
    def get_all(self):
        cur = Cursante.connection.cursor()
        sql = """SELECT * FROM `Cursante`"""

        try:
            cur.execute(sql)
            return {"names": [ desc[0] for desc in cur.description], "data":cur.fetchall()}
            
        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)     

    @classmethod
    def get_register(self, id_register):
        cur = Cursante.connection.cursor()
        sql = """SELECT * FROM `Cursante` WHERE codigo = ?"""

        try:
            cur.execute(sql, (id_register,))
            return cur.fetchone()

        except Exception as e:
            mb.showwarning("Ha ocurrido un problema", e)  

    @classmethod
    def need_update(self):
        Cursante.modified = True

    @classmethod
    def is_update(self):
        return Cursante.modified
    
    @classmethod
    def updated(self):
        Cursante.modified = False


class FormCursante(Cursante, Form):

    def __init__(self):
        Cursante.__init__(self)

        # Al momento de crear la ventana, también la oculta
        self.root = Toplevel()
        self.root.withdraw()
        self.root.resizable(0,0)

        # Al cerrar la ventana, esta sólo se ocultará.
        # Esto evita crearla cada vez que se la necesita.
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

        self.id_register = None

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

        lbl_institute = Label(self.fieldsFrame, text="Institución: ", width=10)
        lbl_institute.grid(row=11, column=0, columnspan=10)

        institute = StringVar()
        e_institute = Combobox(self.fieldsFrame, textvariable=institute, width=37,
                               values=("UNTDF", "UTN", "OTRO"), state="readonly")
        e_institute.current(0)
        e_institute.grid(row=12, column=0, columnspan=40, pady=(0,15))

        Form.__init__(self, {"dni":dni, "nombre":name, "apellido":surname,
                             "email":email, "telefono":phone, "institucion":institute})

        dni.trace("w", lambda *args: self.validate_dni(dni, *args))
        name.trace("w", lambda *args: self.validate_str(name, *args))
        surname.trace("w", lambda *args: self.validate_str(surname, *args))
        email.trace("w", lambda *args: self.validate_email(email, *args))
        phone.trace("w", lambda *args: self.validate_phone(phone, *args))

    def hide(self):
        # Se oculta la ventana
        self.root.withdraw()

class FormDetailsCursante(FormCursante):
    
    def __init__(self):
        FormCursante.__init__(self)

        self.root.title("Detalles del alumno")

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

        # Se muestra la ventana
        self.root.deiconify()


class FormCreateCursante(FormCursante):

    def __init__(self):
        FormCursante.__init__(self)

        self.root.title("Crear alumno")
        
        lbl_newCursante = Label(self.fieldsFrame, text="Formulario de registro")
        lbl_newCursante.grid(row=0, column=0, columnspan=18, pady=(5,10))

        btn_createCursante = Button(self.fieldsFrame, text="Registrar",
                                        command=lambda: self.create(self.get_data()))
        btn_createCursante.grid(row=13, column=0, columnspan=40, pady=5)

    def show(self):
        # Se limpian los campos llamado a la clase padre 'Form'
        self.clean_fields()

        # Se muestra la ventana
        self.root.deiconify()