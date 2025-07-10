# gestor_usuarios.py

class Usuario:
    """
    Clase Usuario que representa a un usuario del sistema.
    Utiliza un constructor para inicializar atributos
    y un destructor para mostrar un mensaje al eliminarse.
    """

    def __init__(self, nombre, correo):
        """
        Constructor que se ejecuta al crear un nuevo objeto Usuario.
        Inicializa los atributos del objeto.
        """
        self.nombre = nombre
        self.correo = correo
        print(f"[+] Usuario creado: {self.nombre} ({self.correo})")

    def mostrar_info(self):
        """Muestra la información del usuario."""
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")

    def __del__(self):
        """
        Destructor que se ejecuta cuando el objeto es destruido.
        Ideal para liberar recursos, cerrar conexiones, etc.
        """
        print(f"[-] Usuario eliminado: {self.nombre}")


# Función principal del programa
def main():
    print("=== Gestión de Usuarios ===")

    # Crear un usuario
    usuario1 = Usuario("Juan Pérez", "juanperez@gmail.com")
    usuario1.mostrar_info()

    # Crear otro usuario
    usuario2 = Usuario("Ana Torres", "ana.torres@gmail.com")
    usuario2.mostrar_info()

    print("Fin del programa.")
    # Aquí termina main. Al finalizar, Python elimina los objetos (llama al destructor automáticamente).

# Ejecutar el programa solo si es el archivo principal
if __name__ == "__main__":
    main()
