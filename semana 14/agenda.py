import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


class Agenda:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")

        # Lista de eventos
        self.eventos = []

        # Treeview para mostrar los eventos
        self.tree = ttk.Treeview(root, columns=("Fecha", "Hora", "Descripción"), show="headings")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame para los campos de entrada
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Fecha (dd/mm/yyyy):").grid(row=0, column=0)
        self.fecha_entry = tk.Entry(frame)
        self.fecha_entry.grid(row=0, column=1)

        tk.Label(frame, text="Hora (HH:MM):").grid(row=0, column=2)
        self.hora_entry = tk.Entry(frame)
        self.hora_entry.grid(row=0, column=3)

        tk.Label(frame, text="Descripción:").grid(row=1, column=0)
        self.descripcion_entry = tk.Entry(frame, width=50)
        self.descripcion_entry.grid(row=1, column=1, columnspan=3)

        # Botones
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar Evento", command=self.agregar_evento).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Eliminar Evento Seleccionado", command=self.eliminar_evento).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Salir", command=root.quit).grid(row=0, column=2, padx=5)

    def validar_fecha(self, texto):
        try:
            return datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            return None

    def validar_hora(self, texto):
        if not texto.strip():  # si no pone nada, se asigna por defecto 12:00
            return datetime.strptime("12:00", "%H:%M").time()

        formatos = ["%H:%M", "%I:%M %p", "%I %p", "%H"]
        for f in formatos:
            try:
                return datetime.strptime(texto.strip(), f).time()
            except:
                continue
        return None

    def agregar_evento(self):
        fecha = self.validar_fecha(self.fecha_entry.get())
        hora = self.validar_hora(self.hora_entry.get())
        descripcion = self.descripcion_entry.get().strip()

        if not fecha:
            messagebox.showerror("Error", "Fecha inválida. Usa formato dd/mm/yyyy.")
            return
        if not hora:
            messagebox.showerror("Error", "Hora inválida. Usa formato HH:MM en 24h o 12h con AM/PM.")
            return
        if not descripcion:
            messagebox.showerror("Error", "La descripción no puede estar vacía.")
            return

        evento = (fecha.strftime("%d/%m/%Y"), hora.strftime("%H:%M"), descripcion)
        self.eventos.append(evento)
        self.tree.insert("", tk.END, values=evento)

        self.fecha_entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)

    def eliminar_evento(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un evento para eliminar.")
            return

        for item in seleccionado:
            valores = self.tree.item(item, "values")
            if valores in self.eventos:
                self.eventos.remove(valores)
            self.tree.delete(item)


if __name__ == "__main__":
    root = tk.Tk()
    app = Agenda(root)
    root.mainloop()

