from tkinter import messagebox
from tkinter.ttk import Frame, Label, Entry, Button
from Form import Form
import sqlite3

class CourseForm(Form):

    def __init__(self, root, connection, form_type, *args, **kwargs):
        self.conn = connection

        self.fieldsFrame = Frame(root, relief="groove", padding=(15,15))
        self.fieldsFrame.grid(row=0, column=0, padx=10, pady=10)


        lbl_name = Label(self.fieldsFrame, text="Nombre: ", width=10)
        lbl_name.grid(row=1, column=0, columnspan=10)

        name = Entry(self.fieldsFrame, width=40)
        name.grid(row=2, column=0, columnspan=40, pady=(0,15))

        lbl_date_start = Label(self.fieldsFrame, text="Fecha de inicio: ", width=15)
        lbl_date_start.grid(row=3, column=0, columnspan=15)

        date_start = Entry(self.fieldsFrame, width=40)
        date_start.grid(row=4, column=0, columnspan=40, pady=(0,15))

        lbl_date_end = Label(self.fieldsFrame, text="Fecha de fin: ", width=15)
        lbl_date_end.grid(row=5, column=0, columnspan=15)

        date_end = Entry(self.fieldsFrame, width=40)
        date_end.grid(row=6, column=0, columnspan=40, pady=(0,15))

        lbl_workload = Label(self.fieldsFrame, text="Carga horaria: ", width=15)
        lbl_workload.grid(row=7, column=0, columnspan=15)

        workload = Entry(self.fieldsFrame, width=40)
        workload.grid(row=8, column=0, columnspan=40, pady=(0,15))

        lbl_place = Label(self.fieldsFrame, text="Lugar: ", width=10)
        lbl_place.grid(row=9, column=0, columnspan=10)

        place = Entry(self.fieldsFrame, width=40)
        place.grid(row=10, column=0, columnspan=40, pady=(0,15))

        Form.__init__(self, {"nombre":name, "fecha_inicio":date_start, "fecha_fin":date_end,
                             "carga_horaria":workload, "lugar_dictado":place})

        if form_type == "details":
            self.btn_modify = Button(self.fieldsFrame, text="Modificar",
                                    command=self.update)
            self.btn_modify.grid(row=11, column=0, columnspan=20, pady=5)

            self.btn_delete = Button(self.fieldsFrame, text="Eliminar",
                                    command=self.delete)
            self.btn_delete.grid(row=11, column=20, columnspan=20, pady=5)

        elif form_type == "create":
            lbl_newStudent = Label(self.fieldsFrame, text="Formulario de registro")
            lbl_newStudent.grid(row=0, column=0, columnspan=18, pady=(5,10))

            self.btn_createStudent = Button(self.fieldsFrame, text="Registrar",
                                            command=self.create)
            self.btn_createStudent.grid(row=11, column=0, columnspan=40, pady=(5,40))

    def create(self):
        cur = self.conn.cursor()
        data = self.get_data()
        sql = """INSERT INTO `Curso` VALUES 
                  (NULL, ?, ?, ?, ?, ?)"""

        try:
            cur.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print(e)
        
        self.modified = True
        self.clean_fields()
        messagebox.showinfo("Información", "El registro se ha creado con éxito!")

    def delete(self):
        if messagebox.askyesnocancel("Confimación", "Está seguro que desea eliminar \nlos datos del curso?"):
            cur = self.conn.cursor()
            sql = """DELETE FROM `Curso` 
                     WHERE codigo = ?"""
            
            try:
                cur.execute(sql, (self.id_register,))
                self.conn.commit()
            except Exception as e:
                print(e)
            
            self.modified = True
            messagebox.showinfo("Información", "El registro se ha eliminado con éxito!")
            

    def update(self):
        if messagebox.askyesnocancel("Confimación", "Está seguro que desea modificar \nlos datos del curso?"):
            cur = self.conn.cursor()
            data = self.get_data()
            data.append(self.id_register)
            sql = """UPDATE `Curso` 
                     SET nombre = ?, fecha_inicio = ?, fecha_fin = ?, carga_horaria = ?, lugar_dictado = ?
                     WHERE codigo = ?"""

            try:
                cur.execute(sql, data)
                self.conn.commit()
            except Exception as e:
                print(e)

            self.modified = True
            messagebox.showinfo("Información", "El registro se ha modificado con éxito!")