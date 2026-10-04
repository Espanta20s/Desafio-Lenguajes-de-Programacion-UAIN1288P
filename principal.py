import os
import tkinter as tk
from tkinter import ttk, messagebox


def limpiar():

    entrada_nombre.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_dni.delete(0, tk.END)


def registrar():

    nombre = entrada_nombre.get().strip()
    edad = entrada_edad.get().strip()
    dni = entrada_dni.get().strip()

    if nombre == "" or edad == "" or dni == "":
        messagebox.showwarning("Advertencia", "Complete todos los campos")
        return

    if os.path.exists("pacientes.txt"):

        with open("pacientes.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("|")

                if len(datos) >= 3 and datos[2] == dni:
                    messagebox.showerror("Error", "El dni ya existe")
                    return

    with open("pacientes.txt", "a", encoding="utf-8") as archivo:
        archivo.write(nombre + "|" + edad + "|" + dni + "\n")

    messagebox.showinfo("Registro", "Paciente registrado correctamente")

    limpiar()
    mostrar()


def mostrar():

    for fila in tabla.get_children():
        tabla.delete(fila)

    if not os.path.exists("pacientes.txt"):
        return

    with open("pacientes.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")

            if len(datos) == 3:
                tabla.insert("", tk.END, values=(datos[0], datos[1], datos[2]))


def seleccionar(event):

    seleccionado = tabla.selection()

    if seleccionado:
        valores = tabla.item(seleccionado, "values")

        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, valores[0])

        entrada_edad.delete(0, tk.END)
        entrada_edad.insert(0, valores[1])

        entrada_dni.delete(0, tk.END)
        entrada_dni.insert(0, valores[2])


def modificar():

    nombre = entrada_nombre.get().strip()
    edad = entrada_edad.get().strip()
    dni = entrada_dni.get().strip()

    if nombre == "" or edad == "" or dni == "":
        messagebox.showwarning("Advertencia", "Seleccione un paciente")
        return

    registros = []
    encontrado = False

    if os.path.exists("pacientes.txt"):

        with open("pacientes.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("|")

                if len(datos) >= 3 and datos[2] == dni:
                    registros.append(nombre + "|" + edad + "|" + dni)
                    encontrado = True

                else:
                    registros.append(linea.strip())

    if encontrado:

        with open("pacientes.txt", "w", encoding="utf-8") as archivo:
            for registro in registros:
                archivo.write(registro + "\n")

        messagebox.showinfo("Modificar", "Paciente modificado")

        limpiar()
        mostrar()


def eliminar():

    dni = entrada_dni.get().strip()

    if dni == "":
        messagebox.showwarning("Advertencia", "Seleccione un paciente")
        return

    respuesta = messagebox.askyesno("Confirmar", "¿Desea eliminar el paciente?")

    if not respuesta:
        return

    registros = []
    encontrado = False

    if os.path.exists("pacientes.txt"):

        with open("pacientes.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("|")

                if len(datos) >= 3 and datos[2] == dni:
                    encontrado = True

                else:
                    registros.append(linea.strip())

    if encontrado:

        with open("pacientes.txt", "w", encoding="utf-8") as archivo:
            for registro in registros:
                archivo.write(registro + "\n")

        messagebox.showinfo("Eliminar", "Paciente eliminado")

        limpiar()
        mostrar()


ventana = tk.Tk()
ventana.title("Sistema de centro de salud del MINSA")
ventana.geometry("650x620")
ventana.resizable(False, False)


pestana = ttk.Notebook(ventana)
pestana.pack(fill="both", expand=True)

pag1 = ttk.Frame(pestana)
pag2 = ttk.Frame(pestana)
pestana.add(pag1, text="Bienvenida")
pestana.add(pag2, text="Registro de Pacientes")

titulo1 = ttk.Label(pag1, text="Sistema del MINSA", font=("Arial", 26, "bold"))
titulo1.pack(pady=80)


ttk.Label(pag1, text="Sistema desarrollado en Python", font=("Arial", 16)).pack()
ttk.Label(pag1, text="Tkinter + TXT", font=("Arial", 16)).pack(pady=5)

botones1 = tk.Frame(pag1)
botones1.pack(pady=20)

tk.Button(
    botones1,
    text="Salir",
    width=10,
    command=lambda: ventana.destroy(),
).grid(row=0, column=0, padx=5)


titulo2 = ttk.Label(pag2, text="Registro de Pacientes", font=("Arial", 16, "bold"))
titulo2.pack(pady=20)


formulario = tk.Frame(pag2)
formulario.pack()

ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)

entrada_nombre = tk.Entry(formulario, width=20)
entrada_nombre.grid(row=0, column=1)

ttk.Label(formulario, text="Edad:").grid(row=1, column=0, padx=10, pady=10)

entrada_edad = tk.Entry(formulario, width=20)
entrada_edad.grid(row=1, column=1)

ttk.Label(formulario, text="DNI:").grid(row=2, column=0, padx=10, pady=10)

entrada_dni = tk.Entry(formulario, width=20)
entrada_dni.grid(row=2, column=1)


botones2 = tk.Frame(pag2)
botones2.pack(pady=20)

tk.Button(botones2, text="Limpiar", width=10, command=limpiar).grid(
    row=0, column=0, padx=20, pady=5
)

tk.Button(botones2, text="Registrar", width=10, command=registrar).grid(
    row=0, column=1, padx=20, pady=5
)

tk.Button(botones2, text="Modificar", width=10, command=modificar).grid(
    row=1, column=0, padx=20, pady=5
)

tk.Button(botones2, text="Eliminar", width=10, command=eliminar).grid(
    row=1, column=1, padx=20, pady=5
)


tk.Label(pag2, text="Pacientes Registrados", font=("Arial", 12, "bold")).pack(pady=5)

tabla = ttk.Treeview(
    pag2,
    columns=("nombre", "edad", "dni"),
    show="headings",
    height=10,
)

tabla.heading("nombre", text="Nombre")
tabla.heading("edad", text="Edad")
tabla.heading("dni", text="DNI")

tabla.column("nombre", width=200)
tabla.column("edad", width=90)
tabla.column("dni", width=180)

tabla.pack()

tabla.bind("<ButtonRelease-1>", seleccionar)

mostrar()

ventana.mainloop()
