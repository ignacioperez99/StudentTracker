from tkinter import messagebox
from tkinter.ttk import Frame, Label, Entry, Button
from Form import Form
import sqlite3

class StudentForm(Form):

    def __init__(self, root, connection, form_type, *args, **kwargs):
        self.conn = connection

        self.fieldsFrame = Frame(root, relief="groove", padding=(15,15))
        self.fieldsFrame.grid(row=0, column=0, padx=10, pady=10)

        lbl_dni = Label(self.fieldsFrame, text="DNI: ", width=10)
        lbl_dni.grid(row=1, column=0, columnspan=10)

        dni = Entry(self.fieldsFrame, width=40)
        dni.grid(row=2, column=0, columnspan=40, pady=(0,15))

        lbl_name = Label(self.fieldsFrame, text="Nombre: ", width=10)
        lbl_name.grid(row=3, column=0, columnspan=10)

        name = Entry(self.fieldsFrame, width=40)
        name.grid(row=4, column=0, columnspan=40, pady=(0,15))

        lbl_surname = Label(self.fieldsFrame, text="Apellido: ", width=10)
        lbl_surname.grid(row=5, column=0, columnspan=10)

        surname = Entry(self.fieldsFrame, width=40)
        surname.grid(row=6, column=0, columnspan=40, pady=(0,15))

        lbl_email = Label(self.fieldsFrame, text="Email: ", width=10)
        lbl_email.grid(row=7, column=0, columnspan=10)

        email = Entry(self.fieldsFrame, width=40)
        email.grid(row=8, column=0, columnspan=40, pady=(0,15))

        lbl_phone = Label(self.fieldsFrame, text="Teléfono: ", width=10)
        lbl_phone.grid(row=9, column=0, columnspan=10)

        phone = Entry(self.fieldsFrame, width=40)
        phone.grid(row=10, column=0, columnspan=40, pady=(0,15))

        lbl_institute = Label(self.fieldsFrame, text="Institución: ", width=10)
        lbl_institute.grid(row=11, column=0, columnspan=10)

        institute = Entry(self.fieldsFrame, width=40)
        institute.grid(row=12, column=0, columnspan=40, pady=(0,15))

        Form.__init__(self, {"dni":dni, "nombre":name, "apellido":surname,
                             "email":email, "telefono":phone, "institucion":institute})

        if form_type == "details":
            self.btn_modify = Button(self.fieldsFrame, text="Modificar",
                                    command=self.update)
            self.btn_modify.grid(row=13, column=0, columnspan=20, pady=5)

            self.btn_delete = Button(self.fieldsFrame, text="Eliminar",
                                    command=self.delete)
            self.btn_delete.grid(row=13, column=20, columnspan=20, pady=5)

        elif form_type == "create":
            lbl_newStudent = Label(self.fieldsFrame, text="Formulario de registro")
            lbl_newStudent.grid(row=0, column=0, columnspan=18, pady=(5,10))

            self.btn_createStudent = Button(self.fieldsFrame, text="Registrar",
                                            command=self.create)
            self.btn_createStudent.grid(row=13, column=0, columnspan=40, pady=5)

    def create(self):
        cur = self.conn.cursor()
        data = self.get_data()
        sql = """INSERT INTO `Cursante` VALUES 
                  (NULL, ?, ?, ?, ?, ?, ?)"""

        try:
            cur.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print(e)
        
        self.modified = True
        self.clean_fields()
        messagebox.showinfo("Información", "El registro se ha creado con éxito!")

    def delete(self):
        if messagebox.askyesnocancel("Confimación", "Está seguro que desea eliminar \nlos datos del alumno?"):
            cur = self.conn.cursor()
            sql = """DELETE FROM `Cursante` 
                     WHERE codigo = ?"""
            
            try:
                cur.execute(sql, (self.id_register,))
                self.conn.commit()
            except Exception as e:
                print(e)
            
            self.modified = True
            messagebox.showinfo("Información", "El registro se ha eliminado con éxito!")
            

    def update(self):
        if messagebox.askyesnocancel("Confimación", "Está seguro que desea modificar \nlos datos del alumno?"):
            cur = self.conn.cursor()
            data = self.get_data()
            data.append(self.id_register)
            sql = """UPDATE `Cursante` 
                     SET dni = ?, nombre = ?, apellido = ?, email = ?, telefono = ?, institucion = ? 
                     WHERE codigo = ?"""

            try:
                cur.execute(sql, data)
                self.conn.commit()
            except Exception as e:
                print(e)

            self.modified = True
            messagebox.showinfo("Información", "El registro se ha modificado con éxito!")