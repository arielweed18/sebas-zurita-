import tkinter as tk
from tkinter import messagebox

# Funciones principales
def agregar_tarea(event=None):
    tarea = entrada_tarea.get().strip()
    if tarea:
        lista_tareas.insert(tk.END, tarea)
        entrada_tarea.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "La tarea no puede estar vacía.")

def marcar_completada(event=None):
    try:
        seleccion = lista_tareas.curselection()[0]
        tarea = lista_tareas.get(seleccion)
        if not tarea.startswith("✔ "):
            lista_tareas.delete(seleccion)
            lista_tareas.insert(seleccion, f"✔ {tarea}")
    except IndexError:
        messagebox.showinfo("Información", "Seleccione una tarea para marcar como completada.")

def eliminar_tarea(event=None):
    try:
        seleccion = lista_tareas.curselection()[0]
        lista_tareas.delete(seleccion)
    except IndexError:
        messagebox.showinfo("Información", "Seleccione una tarea para eliminar.")

def cerrar_app(event=None):
    ventana.destroy()

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Tareas")
ventana.geometry("400x400")

# Campo de entrada y botón para agregar tareas
entrada_tarea = tk.Entry(ventana, width=30)
entrada_tarea.pack(pady=10)
entrada_tarea.focus()

btn_agregar = tk.Button(ventana, text="Agregar Tarea", command=agregar_tarea)
btn_agregar.pack(pady=5)

# Lista de tareas
lista_tareas = tk.Listbox(ventana, width=50, height=15)
lista_tareas.pack(pady=10)

# Botones para marcar y eliminar tareas
btn_completar = tk.Button(ventana, text="Marcar como Completada", command=marcar_completada)
btn_completar.pack(pady=5)

btn_eliminar = tk.Button(ventana, text="Eliminar Tarea", command=eliminar_tarea)
btn_eliminar.pack(pady=5)

# Atajos de teclado
ventana.bind("<Return>", agregar_tarea)       # Enter -> agregar tarea
ventana.bind("c", marcar_completada)          # C -> marcar como completada
ventana.bind("<Delete>", eliminar_tarea)      # Supr -> eliminar tarea
ventana.bind("d", eliminar_tarea)             # D -> eliminar tarea
ventana.bind("<Escape>", cerrar_app)          # Esc -> cerrar aplicación

# Ejecutar la aplicación
ventana.mainloop()
