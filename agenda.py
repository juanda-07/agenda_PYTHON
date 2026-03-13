import json
import tkinter as tk
from tkinter import ttk, messagebox

#archivo donde se guardan los datos
ARCHIVO = "personas.json"

#modelo
class Persona:
    #el contructor que inicializa y guarda los datos del objeto
    def __init__(self, id, nombres, apellidos, fecha, sexo, telefono):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha = fecha
        self.sexo = sexo
        self.telefono = telefono

    #convierte el objeto en un diccionario
    def to_dict(self):
        return self.__dict__


#persistencia
#crea una archivo llamado "ARCHIVO" y si ya existe escribe nuevo contenido 
def cargar():
    try:
        with open(ARCHIVO, "r") as f:
            datos = json.load(f) #convierte los datos a json y los escribe en el archivo
            return [Persona(**d) for d in datos]  
    except:
        return []  
    
def guardar(personas):
    with open(ARCHIVO, "w") as f:
        json.dump([p.to_dict() for p in personas], f, indent=4)


#controlador 
class Controlador:

    def __init__(self):
        self.personas = cargar() 

    # Genera ID automático
    def generar_id(self):
        return f"ID{len(self.personas)+1:03}"

    def agregar(self, n, a, f, s, t):

        id = self.generar_id()

        p = Persona(id, n, a, f, s, t)

        self.personas.append(p)

        guardar(self.personas)

    def eliminar(self, id):

        self.personas = [p for p in self.personas if p.id != id]

        guardar(self.personas)

    def buscar(self, texto):

        return [p for p in self.personas if texto.lower() in p.nombres.lower()]

#vista
class Vista:

    def __init__(self, root, ctrl):

        self.ctrl = ctrl
        root.title("Agenda de Personas")

        # Campos de entrada
        self.nom = tk.Entry(root)
        self.ape = tk.Entry(root)
        self.fecha = tk.Entry(root)

        self.sexo = ttk.Combobox(root, values=["Masculino", "Femenino"], state="readonly")
        self.sexo.current(0)

        self.tel = tk.Entry(root)
        self.buscar = tk.Entry(root)

        labels = ["Nombres", "Apellidos", "Fecha", "Sexo", "Telefono"]

        for i, l in enumerate(labels):
            tk.Label(root, text=l).grid(row=i, column=0)

        self.nom.grid(row=0, column=1)
        self.ape.grid(row=1, column=1)
        self.fecha.grid(row=2, column=1)
        self.sexo.grid(row=3, column=1)
        self.tel.grid(row=4, column=1)

        tk.Label(root, text="Buscar").grid(row=5, column=0)
        self.buscar.grid(row=5, column=1)

        tk.Button(root, text="Guardar", command=self.guardar).grid(row=6, column=0)
        tk.Button(root, text="Buscar", command=self.buscar_persona).grid(row=6, column=1)
        tk.Button(root, text="Eliminar", command=self.eliminar).grid(row=6, column=2)
        tk.Button(root, text="Salir", command=root.quit).grid(row=6, column=3)

        #tabla donde se mue4stran los registros en la interfaz grafica
        self.tabla = ttk.Treeview(root, columns=("id","nom","ape","fecha","sexo","tel"), show="headings")

        for c in ("id","nom","ape","fecha","sexo","tel"):
            self.tabla.heading(c, text=c)

        self.tabla.grid(row=7, column=0, columnspan=4)

        self.actualizar()


    def actualizar(self):

        for i in self.tabla.get_children():
            self.tabla.delete(i)

        for p in self.ctrl.personas:
            self.tabla.insert("", tk.END, values=(p.id, p.nombres, p.apellidos, p.fecha, p.sexo, p.telefono))


    def guardar(self):

        self.ctrl.agregar(
            self.nom.get(),
            self.ape.get(),
            self.fecha.get(),
            self.sexo.get(),
            self.tel.get()
        )

        self.actualizar()


    def buscar_persona(self):

        res = self.ctrl.buscar(self.buscar.get())

        for i in self.tabla.get_children():
            self.tabla.delete(i)

        for p in res:
            self.tabla.insert("", tk.END, values=(p.id, p.nombres, p.apellidos, p.fecha, p.sexo, p.telefono))

    def eliminar(self):

        item = self.tabla.selection()

        if not item:
            messagebox.showwarning("Error","Seleccione una persona")
            return

        id = self.tabla.item(item)["values"][0]

        self.ctrl.eliminar(id)

        self.actualizar()


#main
root = tk.Tk()

ctrl = Controlador()

app = Vista(root, ctrl)

root.mainloop()