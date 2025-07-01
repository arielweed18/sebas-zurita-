#  Aplicación de POO en Python
# Sistema de gestión de vehículos

# Clase base: Vehiculo
class Vehiculo:
    def __init__(self, marca, modelo, velocidad_maxima):
        self.marca = marca
        self.modelo = modelo
        self._velocidad_maxima = velocidad_maxima  # Atributo encapsulado

    def describir(self):
        return f"Vehiculo {self.marca} {self.modelo}"

    def get_velocidad_maxima(self):
        return self._velocidad_maxima

    def set_velocidad_maxima(self, nueva_velocidad):
        if nueva_velocidad > 0:
            self._velocidad_maxima = nueva_velocidad

# Clase derivada: Auto (hereda de Vehiculo)
class Auto(Vehiculo):
    def __init__(self, marca, modelo, velocidad_maxima, puertas):
        super().__init__(marca, modelo, velocidad_maxima)
        self.puertas = puertas

    def describir(self):  # Polimorfismo (método sobrescrito)
        return f"Auto {self.marca} {self.modelo} con {self.puertas} puertas"

# Clase derivada: Moto (hereda de Vehiculo)
class Moto(Vehiculo):
    def __init__(self, marca, modelo, velocidad_maxima, tipo):
        super().__init__(marca, modelo, velocidad_maxima)
        self.tipo = tipo  # Ej: deportiva, scooter, etc.

    def describir(self):  # Polimorfismo (método sobrescrito)
        return f"Moto {self.marca} {self.modelo} tipo {self.tipo}"

# Crear instancias y usar los métodos
vehiculos = [
    Auto("Toyota", "Corolla", 180, 4),
    Moto("Yamaha", "R1", 299, "Deportiva"),
    Auto("Tesla", "Model 3", 250, 4)
]

# Mostrar descripciones y velocidades
for v in vehiculos:
    print(v.describir())
    print(f"Velocidad máxima: {v.get_velocidad_maxima()} km/h\n")
