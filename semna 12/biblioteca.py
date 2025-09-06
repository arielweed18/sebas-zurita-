# ===============================
# Sistema de Gestión de Biblioteca Digital
# ===============================

# Clase Libro
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        # Tupla inmutable con (titulo, autor)
        self.datos = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"{self.datos[0]} - {self.datos[1]} (Categoría: {self.categoria}, ISBN: {self.isbn})"


# Clase Usuario
class Usuario:
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        self.libros_prestados = []  # lista de libros prestados

    def prestar_libro(self, libro):
        self.libros_prestados.append(libro)

    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            self.libros_prestados.remove(libro)

    def listar_libros(self):
        if not self.libros_prestados:
            return f"El usuario {self.nombre} no tiene libros prestados."
        return f"Libros prestados a {self.nombre}:\n" + "\n".join([str(libro) for libro in self.libros_prestados])

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.user_id})"


# Clase Biblioteca
class Biblioteca:
    def __init__(self):
        self.libros = {}       # diccionario {isbn: objeto Libro}
        self.usuarios = {}     # diccionario {user_id: objeto Usuario}
        self.ids_usuarios = set()  # conjunto para asegurar IDs únicos

    # --- Gestión de libros ---
    def añadir_libro(self, libro):
        if libro.isbn not in self.libros:
            self.libros[libro.isbn] = libro
            print(f"Libro añadido: {libro}")
        else:
            print("El libro ya existe en la biblioteca.")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            eliminado = self.libros.pop(isbn)
            print(f"Libro eliminado: {eliminado}")
        else:
            print("No se encontró el libro con ese ISBN.")

    # --- Gestión de usuarios ---
    def registrar_usuario(self, usuario):
        if usuario.user_id not in self.ids_usuarios:
            self.usuarios[usuario.user_id] = usuario
            self.ids_usuarios.add(usuario.user_id)
            print(f"Usuario registrado: {usuario}")
        else:
            print("Ya existe un usuario con ese ID.")

    def dar_baja_usuario(self, user_id):
        if user_id in self.usuarios:
            eliminado = self.usuarios.pop(user_id)
            self.ids_usuarios.remove(user_id)
            print(f"Usuario eliminado: {eliminado}")
        else:
            print("Usuario no encontrado.")

    # --- Préstamos ---
    def prestar_libro(self, user_id, isbn):
        if user_id in self.usuarios and isbn in self.libros:
            usuario = self.usuarios[user_id]
            libro = self.libros.pop(isbn)  # lo quitamos de la biblioteca
            usuario.prestar_libro(libro)
            print(f"Libro prestado: {libro} a {usuario.nombre}")
        else:
            print("No se pudo realizar el préstamo (usuario o libro no encontrado).")

    def devolver_libro(self, user_id, isbn):
        if user_id in self.usuarios:
            usuario = self.usuarios[user_id]
            for libro in usuario.libros_prestados:
                if libro.isbn == isbn:
                    usuario.devolver_libro(libro)
                    self.libros[isbn] = libro  # vuelve a la biblioteca
                    print(f"Libro devuelto: {libro}")
                    return
        print("No se pudo devolver el libro.")

    # --- Búsquedas ---
    def buscar_por_titulo(self, titulo):
        return [libro for libro in self.libros.values() if libro.datos[0].lower() == titulo.lower()]

    def buscar_por_autor(self, autor):
        return [libro for libro in self.libros.values() if libro.datos[1].lower() == autor.lower()]

    def buscar_por_categoria(self, categoria):
        return [libro for libro in self.libros.values() if libro.categoria.lower() == categoria.lower()]

    # --- Mostrar libros prestados ---
    def libros_prestados_usuario(self, user_id):
        if user_id in self.usuarios:
            print(self.usuarios[user_id].listar_libros())
        else:
            print("Usuario no encontrado.")

if __name__ == "__main__":
    # Crear biblioteca
    biblio = Biblioteca()

    # Crear libros
    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", "Novela", "12345")
    libro2 = Libro("El Principito", "Antoine de Saint-Exupéry", "Infantil", "67890")
    libro3 = Libro("Python para Todos", "Raúl González", "Tecnología", "11111")

    # Añadir libros
    biblio.añadir_libro(libro1)
    biblio.añadir_libro(libro2)
    biblio.añadir_libro(libro3)

    # Crear usuarios
    usuario1 = Usuario("Ana", "U001")
    usuario2 = Usuario("Luis", "U002")

    # Registrar usuarios
    biblio.registrar_usuario(usuario1)
    biblio.registrar_usuario(usuario2)

    # Prestar libro
    biblio.prestar_libro("U001", "12345")

    # Ver libros prestados
    biblio.libros_prestados_usuario("U001")

    # Devolver libro
    biblio.devolver_libro("U001", "12345")

    # Buscar por autor
    resultado = biblio.buscar_por_autor("Antoine de Saint-Exupéry")
    print("Resultado búsqueda por autor:", [str(r) for r in resultado])



