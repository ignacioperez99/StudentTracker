import re, os, csv, tkinter as tk
from tkinter import Tk, messagebox, filedialog, Toplevel, Menu, StringVar, IntVar
from tkinter.ttk import Combobox, Frame, Label, Entry, Button, Notebook, LabelFrame


class Application(Tk):

    def __init__(self, *args, **kwargs):
        """ Se ejecuta al crear una instancia de la clase """
        self.root = Tk()
        self.root.title("Sistema de Gestión de Alumnos")
        self.root.geometry("600x500")
        self.root.resizable(0,0)
        self.root.option_add('*tearOff', False)
        self.create_widgets()
        self.create_window_login()
        self.root.mainloop()

    def create_widgets(self):
        self.processes = []

        toolbar = Menu(self.root)
        self.root['menu'] = toolbar

        self.menu_opciones = Menu(toolbar)
        self.menu_ayuda = Menu(toolbar)
        toolbar.add_cascade(menu=self.menu_opciones, label='Opciones')
        toolbar.add_cascade(menu=self.menu_ayuda, label='Ayuda')
                 
        self.menu_opciones.add_command(label='Procesos...', 
                               command=self.show_data_processes)

        self.otherFrame = LabelFrame(self.root, text="algo", relief="groove", padding=(20, 10))
        self.otherFrame.grid(column=0, row=1, columnspan=1, padx=10, pady=10)

        lbl_policies = Label(self.otherFrame, text="Política de planificación: ")
        lbl_policies.grid(column=0, row=0, columnspan=10)

        self.policies = Combobox(self.otherFrame, state="readonly", width=33)
        self.policies['values'] = ("FCFS (First Come First Served)", "Prioridad Externa", "Round-Robin", "SPN (Shortest Process Next)", "SRTN (Shortest Remaining Time Next)")
        self.policies.current(0)
        self.policies.grid(column=0, row=1, columnspan=2, pady=5)

        lbl_tip = Label(self.otherFrame, text="TIP: ")
        lbl_tip.grid(column=0, row=2,  pady=5)

        self.tip = Entry(self.otherFrame, width=25)
        self.tip.grid(column=1, row=2, pady=10)

        lbl_tfp = Label(self.otherFrame, text="TFP: ")
        lbl_tfp.grid(column=0, row=3, pady=10)

        self.tfp = Entry(self.otherFrame, width=25)
        self.tfp.grid(column=1, row=3, pady=10)

        lbl_tcp = Label(self.otherFrame, text="TPC: ")
        lbl_tcp.grid(column=0, row=4, pady=10)

        self.tcp = Entry(self.otherFrame, width=25)
        self.tcp.grid(column=1, row=4, pady=10)

        lbl_quantum = Label(self.otherFrame, text="Quantum: ")
        lbl_quantum.grid(column=0, row=5)

        self.quantum = Entry(self.otherFrame, width=25)
        self.quantum.grid(column=1, row=5, pady=10)        

    def create_window_login(self, *args, **kwargs):
        self.root.withdraw()
        self.win_login = Toplevel()
        self.win_login.title("Inicio de sesión")
        self.win_login.resizable(0,0)
        self.win_login.protocol("WM_DELETE_WINDOW", self.root.destroy)

        lbl_user = Label(self.win_login, text="Usuario: ")
        lbl_user.grid(row=0, column=0, padx=(20,10), pady=(10,0))

        self.e_user = Entry(self.win_login, width=25)
        self.e_user.grid(row=0, column=1, padx=(10,20), pady=(20,10)) 
        self.e_user.focus_set()

        lbl_password = Label(self.win_login, text="Contraseña: ")
        lbl_password.grid(row=2, column=0, padx=(20,10))

        self.e_password = Entry(self.win_login, width=25)
        self.e_password.grid(row=2, column=1, padx=(10,20), pady=10) 

        btn_login = Button(self.win_login, text="Ingresar", command=self.login)
        btn_login.grid(row=3, column=0, columnspan=3, padx=10, pady=(5,20))

    def login(self):
        # Lógica de logueo

        self.win_login.withdraw()
        self.root.update()
        self.root.deiconify()

    def show_data_processes(self):
        self.processTable.update()
        self.processTable.deiconify()

    def hide_data_processes(self):
        self.processTable.withdraw()
        self.root.update()
        self.root.deiconify()

    """ def add_process(self):
        aux_frame = Frame(self.tableFrame)
        
        task = Proceso(StringVar(), IntVar(), IntVar(), IntVar(), IntVar(), 1)
        self.processes.append(task)

        e_name     = Entry(aux_frame, textvariable=task.nombre, width=20)
        e_name.grid(row=0, column=0)
        e_arrival  = Entry(aux_frame, textvariable=task.nombre, width=10)
        e_arrival.grid(row=0, column=1)
        e_burstF   = Entry(aux_frame, textvariable=task.nombre, width=10)
        e_burstF.grid(row=0, column=2)
        e_burstIO  = Entry(aux_frame, textvariable=task.nombre, width=10)
        e_burstIO.grid(row=0, column=3)
        e_priority = Entry(aux_frame, textvariable=task.nombre, width=10)
        e_priority.grid(row=0, column=4)

        aux_frame.pack() """
        
    def create_window_processes(self):
        self.processTable = Toplevel()
        self.processTable.title("Datos de Procesos")
        self.processTable.resizable(0,0)

        self.tableFrame = Frame(self.processTable, relief="groove", padding=(20, 10))
        self.tableFrame.grid(column=0, row=1, columnspan=70, padx=10, pady=10)
    
        auxx_frame = Frame(self.tableFrame)

        lbl_name = Label(auxx_frame, text="Nombre")
        lbl_name.pack()
        
        lbl_arrival = Label(auxx_frame, text="Arribo")
        lbl_arrival.pack()
        
        lbl_burstToFinish = Label(auxx_frame, text="Terminar")
        lbl_burstToFinish.pack()
        
        lbl_burstCPU = Label(auxx_frame, text="CPU")
        lbl_burstCPU.pack()
        
        lbl_burstIO = Label(auxx_frame, text="E/S")
        lbl_burstIO.pack()
        
        lbl_priority = Label(auxx_frame, text="Prioridad")
        lbl_priority.pack()

        btn_add_process = Button(self.processTable, text="[+] Agregar proceso", command=self.add_process)
        btn_add_process.grid(column=0, row=0, padx=10, pady=(5,20))

        self.hide_data_processes()

if __name__ == "__main__":
    app = Application()
