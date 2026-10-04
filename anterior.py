import tkinter as tk
from tkinter import messagebox


class Paciente:

    def __init__(self, nombre, edad, dni):
        self.nombre = nombre
        self.edad = edad
        self.dni = dni


pacientes = []


# Cargar pacientes guardados al iniciar
def cargar_pacientes():
    try:
        with open("pacientes.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()

                if linea:
                    datos = linea.split("|")

                    if len(datos) == 3:
                        nombre, edad, dni = datos

                        paciente = Paciente(nombre, edad, dni)
                        pacientes.append(paciente)

                        lista_pacientes.insert(
                            tk.END, f"{paciente.nombre} - Edad: {paciente.edad}"
                        )

    except FileNotFoundError:
        # Si el archivo no existe, no pasa nada.
        pass


def registrar_paciente():

    nombre = entrada_nombre.get().strip()
    edad = entrada_edad.get().strip()
    dni = entrada_dni.get().strip()

    # Comprobar campos vacíos
    if nombre == "" or edad == "" or dni == "":
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    # Comprobar edad
    if not edad.isdigit():
        messagebox.showerror("Error", "La edad debe ser un número")
        return

    # Comprobar DNI
    if not dni.isdigit() or len(dni) != 8:
        messagebox.showerror("Error", "El DNI debe tener 8 números")
        return

    # Comprobar si el DNI ya está registrado
    for paciente in pacientes:
        if paciente.dni == dni:
            messagebox.showerror(
                "Paciente duplicado", "Ya existe un paciente registrado con ese DNI."
            )
            return

    # Crear paciente
    paciente = Paciente(nombre, edad, dni)

    # Agregar a la lista
    pacientes.append(paciente)

    # Guardar en el archivo TXT
    with open("pacientes.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{paciente.nombre}|{paciente.edad}|{paciente.dni}\n")

    # Mostrar en la lista
    lista_pacientes.insert(tk.END, f"{paciente.nombre} - Edad: {paciente.edad}")

    # Limpiar campos
    entrada_nombre.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_dni.delete(0, tk.END)

    messagebox.showinfo("Correcto", "Paciente registrado correctamente")


# Ventana principal
ventana = tk.Tk()
ventana.title("Hospital paso al infierno")
ventana.geometry("500x500")


titulo = tk.Label(ventana, text="Registro de Pacientes", font=("Arial", 16))
titulo.pack(pady=10)


tk.Label(ventana, text="Nombre:").pack()

entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack()


tk.Label(ventana, text="Edad:").pack()

entrada_edad = tk.Entry(ventana)
entrada_edad.pack()


tk.Label(ventana, text="DNI:").pack()

entrada_dni = tk.Entry(ventana)
entrada_dni.pack()


boton_registrar = tk.Button(
    ventana, text="Registrar paciente", width=20, command=registrar_paciente
)
boton_registrar.pack(pady=10)


boton_salir = tk.Button(
    ventana, text="Salir", width=10, command=lambda: ventana.destroy()
)
boton_salir.pack(pady=15)


tk.Label(ventana, text="Pacientes registrados:").pack()


lista_pacientes = tk.Listbox(ventana, width=55, height=10)
lista_pacientes.pack(pady=10)


# Cargar pacientes del archivo al iniciar
cargar_pacientes()


ventana.mainloop()
