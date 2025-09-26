import tkinter as tk
from tkinter import messagebox


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas - GUI con Tkinter")
        self.root.geometry("400x400")

        # ---------- Entrada de nueva tarea ----------
        self.task_entry = tk.Entry(self.root, width=35)
        self.task_entry.pack(pady=10)

        # Permitir añadir tarea con la tecla Enter
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # ---------- Botones ----------
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        self.add_button = tk.Button(button_frame, text="Añadir Tarea", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)

        self.complete_button = tk.Button(button_frame, text="Marcar Completada", command=self.complete_task)
        self.complete_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(button_frame, text="Eliminar Tarea", command=self.delete_task)
        self.delete_button.grid(row=0, column=2, padx=5)

        # ---------- Lista de tareas ----------
        self.task_listbox = tk.Listbox(self.root, width=50, height=15, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        # Evento opcional: doble clic para marcar completada
        self.task_listbox.bind("<Double-1>", lambda event: self.complete_task())

    # ---------- Funciones principales ----------
    def add_task(self):
        task = self.task_entry.get().strip()
        if task != "":
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrada vacía", "Por favor, escribe una tarea antes de añadir.")

    def complete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(index)

            # Verificar si ya está completada
            if task.startswith("[✔]"):
                messagebox.showinfo("Aviso", "La tarea ya está marcada como completada.")
            else:
                self.task_listbox.delete(index)
                self.task_listbox.insert(index, f"[✔] {task}")
        except IndexError:
            messagebox.showwarning("Selección inválida", "Por favor, selecciona una tarea de la lista.")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(index)
        except IndexError:
            messagebox.showwarning("Selección inválida", "Por favor, selecciona una tarea para eliminar.")


# ---------- Ejecutar la aplicación ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
