import os
import tkinter as tk
from tkinter import ttk, messagebox


ARCHIVO = "pacientes.txt"


def limpiar():

    entrada_nombre.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_dni.delete(0, tk.END)
    entrada_telefono.delete(0, tk.END)


def validar_datos(nombre, edad, dni, telefono):

    if nombre == "" or edad == "" or dni == "" or telefono == "":
        messagebox.showwarning("Advertencia", "Complete todos los campos")
        return False

    if not nombre.replace(" ", "").isalpha():
        messagebox.showwarning("Advertencia", "El nombre solo debe contener letras")
        return False

    if not edad.isdigit() or not 1 <= int(edad) <= 120:
        messagebox.showwarning("Advertencia", "La edad debe estar entre 1 y 120")
        return False

    if not dni.isdigit() or len(dni) != 8:
        messagebox.showwarning("Advertencia", "El DNI debe tener 8 digitos")
        return False

    if not telefono.isdigit() or len(telefono) != 9:
        messagebox.showwarning("Advertencia", "El telefono debe tener 9 digitos")
        return False

    return True


def obtener_registros():

    registros = []

    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    datos = linea.strip().split("|")

                    if len(datos) == 4:
                        registros.append(datos)
        except OSError:
            messagebox.showerror("Error", "No se pudo leer el archivo de pacientes")

    return registros


def guardar_registros(registros):

    try:
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            for registro in registros:
                archivo.write("|".join(registro) + "\n")
    except OSError:
        messagebox.showerror("Error", "No se pudo guardar la informacion")


def registrar():

    nombre = entrada_nombre.get().strip()
    edad = entrada_edad.get().strip()
    dni = entrada_dni.get().strip()
    telefono = entrada_telefono.get().strip()

    if not validar_datos(nombre, edad, dni, telefono):
        return

    registros = obtener_registros()

    # FILTER: busca si existe un paciente con el mismo DNI.
    duplicados = list(filter(lambda paciente: paciente[2] == dni, registros))

    if duplicados:
        messagebox.showerror("Error", "El DNI ya existe")
        return

    registros.append([nombre, edad, dni, telefono])
    guardar_registros(registros)

    messagebox.showinfo("Registro", "Paciente registrado correctamente")

    limpiar()
    mostrar()


def mostrar(registros=None):

    for fila in tabla.get_children():
        tabla.delete(fila)

    if registros is None:
        registros = obtener_registros()

    # MAP: transforma cada registro en los valores que se muestran en la tabla.
    datos_tabla = list(
        map(
            lambda paciente: (paciente[0], paciente[1], paciente[2], paciente[3]),
            registros,
        )
    )

    for datos in datos_tabla:
        tabla.insert("", tk.END, values=datos)


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

        entrada_telefono.delete(0, tk.END)
        entrada_telefono.insert(0, valores[3])


def modificar():

    nombre = entrada_nombre.get().strip()
    edad = entrada_edad.get().strip()
    dni = entrada_dni.get().strip()
    telefono = entrada_telefono.get().strip()

    if not validar_datos(nombre, edad, dni, telefono):
        return

    registros = obtener_registros()
    encontrado = False

    for registro in registros:
        if registro[2] == dni:
            registro[0] = nombre
            registro[1] = edad
            registro[3] = telefono
            encontrado = True
            break

    if encontrado:
        guardar_registros(registros)
        messagebox.showinfo("Modificar", "Paciente modificado correctamente")

        limpiar()
        mostrar()
    else:
        messagebox.showwarning("Modificar", "No se encontro el paciente")


def eliminar():

    dni = entrada_dni.get().strip()

    if dni == "":
        messagebox.showwarning("Advertencia", "Seleccione un paciente")
        return

    respuesta = messagebox.askyesno("Confirmar", "¿Desea eliminar el paciente?")

    if not respuesta:
        return

    registros = obtener_registros()

    # FILTER: conserva todos los pacientes excepto el que se desea eliminar.
    nuevos_registros = list(filter(lambda paciente: paciente[2] != dni, registros))

    if len(nuevos_registros) == len(registros):
        messagebox.showwarning("Eliminar", "No se encontro el paciente")
        return

    guardar_registros(nuevos_registros)

    messagebox.showinfo("Eliminar", "Paciente eliminado correctamente")

    limpiar()
    mostrar()


def buscar():
    texto = entrada_busqueda.get().strip().lower()

    registros = obtener_registros()

    if texto == "":
        mostrar(registros)
        return

    # FILTER: selecciona pacientes cuyo nombre o DNI coincide con la búsqueda.
    filtrados = list(
        filter(
            lambda paciente: texto in paciente[0].lower() or texto in paciente[2],
            registros,
        )
    )

    mostrar(filtrados)


def mostrar_resumen():
    registros = obtener_registros()

    if not registros:
        messagebox.showinfo("Resumen", "No hay pacientes registrados")
        return

    # MAP: obtiene las edades como números.
    edades = list(map(lambda paciente: int(paciente[1]), registros))

    # REDUCE: suma todas las edades.
    suma_edades = reduce(lambda total, edad: total + edad, edades, 0)

    promedio = suma_edades / len(edades)

    messagebox.showinfo(
        "Resumen",
        f"Pacientes registrados: {len(registros)}\n"
        f"Promedio de edad: {promedio:.1f} años",
    )


ventana = tk.Tk()
ventana.title("Sistema de Centro de Salud del MINSA")
ventana.geometry("760x700")
ventana.resizable(False, False)


pestana = ttk.Notebook(ventana)
pestana.pack(fill="both", expand=True)

pag1 = ttk.Frame(pestana)
pag2 = ttk.Frame(pestana)
pestana.add(pag1, text="Bienvenida")
pestana.add(pag2, text="Registro de Pacientes")

# Bienvenida

titulo1 = ttk.Label(pag1, text="Sistema de Centro de Salud", font=("Arial", 26, "bold"))
titulo1.pack(pady=80)


ttk.Label(
    pag1, text="Sistema desarrollado en Python con Tkinter", font=("Arial", 18)
).pack()
ttk.Label(pag1, text="Registro y gestión de pacientes", font=("Arial", 16)).pack(pady=5)


tk.Button(pag1, text="Salir", width=10, command=ventana.destroy).pack(pady=140)

# Registro de pacientes

titulo2 = ttk.Label(pag2, text="Registro de Pacientes", font=("Arial", 16, "bold"))
titulo2.pack(pady=20)


formulario = tk.Frame(pag2)
formulario.pack()

ttk.Label(formulario, text="Nombres:").grid(
    row=0, column=0, padx=10, pady=10, sticky="e"
)

entrada_nombre = tk.Entry(formulario, width=20)
entrada_nombre.grid(row=0, column=1)

ttk.Label(formulario, text="Edad:").grid(row=1, column=0, padx=10, pady=10, sticky="e")

entrada_edad = tk.Entry(formulario, width=20)
entrada_edad.grid(row=1, column=1)

ttk.Label(formulario, text="DNI:").grid(row=2, column=0, padx=10, pady=10, sticky="e")

entrada_dni = tk.Entry(formulario, width=20)
entrada_dni.grid(row=2, column=1)

ttk.Label(formulario, text="Telefono:").grid(
    row=3, column=0, padx=10, pady=10, sticky="e"
)

entrada_telefono = tk.Entry(formulario, width=20)
entrada_telefono.grid(row=3, column=1)


botones2 = tk.Frame(pag2)
botones2.pack(pady=20)

tk.Button(botones2, text="Limpiar", width=10, command=limpiar).grid(
    row=0, column=0, padx=20, pady=5
)

tk.Button(botones2, text="Registrar", width=10, command=registrar).grid(
    row=0, column=1, padx=20, pady=5
)

tk.Button(botones2, text="Modificar", width=10, command=modificar).grid(
    row=0, column=2, padx=20, pady=5
)

tk.Button(botones2, text="Eliminar", width=10, command=eliminar).grid(
    row=0, column=3, padx=20, pady=5
)

# Botones tabla

tk.Label(pag2, text="Pacientes Registrados", font=("Arial", 14, "bold")).pack(pady=10)


busqueda = tk.Frame(pag2)
busqueda.pack(pady=15)

ttk.Label(busqueda, text="Buscar paciente (nombre/DNI):").grid(
    row=0, column=0, padx=10, pady=10, sticky="e"
)

entrada_busqueda = tk.Entry(busqueda, width=20)
entrada_busqueda.grid(row=0, column=1)

tk.Button(busqueda, text="Buscar", width=10, command=buscar).grid(
    row=0, column=2, padx=20, pady=5
)

tk.Button(busqueda, text="Mostrar todos", width=10, command=lambda: mostrar()).grid(
    row=0, column=3, padx=5
)

tk.Button(busqueda, text="Resumen", width=10, command=mostrar_resumen).grid(
    row=0, column=4, padx=5
)

# Tabla

tabla = ttk.Treeview(
    pag2, columns=("nombre", "edad", "dni", "telefono"), show="headings", height=10
)

tabla.heading("nombre", text="Nombre")
tabla.heading("edad", text="Edad")
tabla.heading("dni", text="DNI")
tabla.heading("telefono", text="Telefono")

tabla.column("nombre", width=200)
tabla.column("edad", width=80)
tabla.column("dni", width=140)
tabla.column("telefono", width=140)

tabla.pack()

tabla.bind("<ButtonRelease-1>", seleccionar)

mostrar()

ventana.mainloop()
