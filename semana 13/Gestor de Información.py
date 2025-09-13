import tkinter as tk
from tkinter import messagebox

# Función para agregar datos a la lista
def agregar_dato():
    dato = entrada_texto.get()  # Obtiene el texto del campo de entrada
    if dato.strip() != "":      # Verifica que no esté vacío
        lista_datos.insert(tk.END, dato)  # Agrega a la Listbox
        entrada_texto.delete(0, tk.END)   # Limpia el campo de entrada
    else:
        messagebox.showwarning("Aviso", "Por favor ingrese un dato válido.")

# Función para limpiar los datos seleccionados
def limpiar_seleccion():
    seleccion = lista_datos.curselection()
    if seleccion:
        for index in reversed(seleccion):
            lista_datos.delete(index)
    else:
        messagebox.showinfo("Información", "No hay elementos seleccionados para eliminar.")

# Función para limpiar toda la lista
def limpiar_todo():
    lista_datos.delete(0, tk.END)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Información")
ventana.geometry("400x300")  # Tamaño de la ventana

# Crear componentes
etiqueta = tk.Label(ventana, text="Ingrese un dato:")
entrada_texto = tk.Entry(ventana, width=30)
boton_agregar = tk.Button(ventana, text="Agregar", command=agregar_dato)
lista_datos = tk.Listbox(ventana, selectmode=tk.MULTIPLE, width=50)
boton_limpiar_seleccion = tk.Button(ventana, text="Limpiar Selección", command=limpiar_seleccion)
boton_limpiar_todo = tk.Button(ventana, text="Limpiar Todo", command=limpiar_todo)

# Ubicar componentes en la ventana
etiqueta.pack(pady=5)
entrada_texto.pack(pady=5)
boton_agregar.pack(pady=5)
lista_datos.pack(pady=10)
boton_limpiar_seleccion.pack(pady=5)
boton_limpiar_todo.pack(pady=5)

# Iniciar la ventana
ventana.mainloop()
