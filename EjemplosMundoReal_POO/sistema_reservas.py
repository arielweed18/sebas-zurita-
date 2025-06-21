class Cliente:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula

    def __str__(self):
        return f"{self.nombre} (Cédula: {self.cedula})"

class Habitacion:
    def __init__(self, numero, tipo, precio):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Habitación {self.numero} - {self.tipo} - ${self.precio} - {estado}"

class Reserva:
    def __init__(self, cliente, habitacion):
        self.cliente = cliente
        self.habitacion = habitacion

    def confirmar(self):
        if self.habitacion.disponible:
            self.habitacion.disponible = False
            print(f"Reserva confirmada para {self.cliente} en la {self.habitacion}")
        else:
            print(f"La habitación {self.habitacion.numero} no está disponible.")

if __name__ == "__main__":
    cliente1 = Cliente("Leon Messi", "0102030405")
    hab1 = Habitacion(10, "Familiar", 1250)
    print(hab1)
    reserva1 = Reserva(cliente1, hab1)
    reserva1.confirmar()
