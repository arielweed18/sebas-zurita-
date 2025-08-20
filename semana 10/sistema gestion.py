import os


class Producto:
    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.codigo},{self.nombre},{self.cantidad},{self.precio}"


class Inventario:
    def __init__(self, archivo="inventario.txt"):
        self.archivo = archivo
        self.productos = {}
        self.cargar_desde_archivo()

    # ------------------ Manejo de Archivos ------------------ #
    def cargar_desde_archivo(self):
        """Carga los productos desde el archivo de inventario"""
        if not os.path.exists(self.archivo):
            # Si no existe, lo crea vacío
            open(self.archivo, "w").close()
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    try:
                        codigo, nombre, cantidad, precio = linea.strip().split(",")
                        self.productos[codigo] = Producto(
                            codigo, nombre, int(cantidad), float(precio)
                        )
                    except ValueError:
                        print("⚠ Error: una línea del archivo está corrupta y será ignorada.")
        except FileNotFoundError:
            print("⚠ Archivo no encontrado. Se creará automáticamente.")
        except PermissionError:
            print("❌ No se tienen permisos para leer el archivo.")

    def guardar_en_archivo(self):
        """Guarda los productos en el archivo de inventario"""
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                for producto in self.productos.values():
                    f.write(str(producto) + "\n")
        except PermissionError:
            print("❌ No se tienen permisos para escribir en el archivo.")
        except Exception as e:
            print(f"❌ Error inesperado al guardar: {e}")

    # ------------------ Operaciones ------------------ #
    def agregar_producto(self, codigo, nombre, cantidad, precio):
        if codigo in self.productos:
            print("⚠ El producto ya existe. Use actualizar en su lugar.")
            return
        self.productos[codigo] = Producto(codigo, nombre, cantidad, precio)
        self.guardar_en_archivo()
        print("✅ Producto agregado y guardado correctamente.")

    def actualizar_producto(self, codigo, cantidad=None, precio=None):
        if codigo not in self.productos:
            print("⚠ Producto no encontrado.")
            return
        if cantidad is not None:
            self.productos[codigo].cantidad = cantidad
        if precio is not None:
            self.productos[codigo].precio = precio
        self.guardar_en_archivo()
        print("✅ Producto actualizado y guardado correctamente.")

    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            del self.productos[codigo]
            self.guardar_en_archivo()
            print("✅ Producto eliminado correctamente.")
        else:
            print("⚠ Producto no encontrado.")

    def mostrar_inventario(self):
        if not self.productos:
            print("📂 Inventario vacío.")
        else:
            print("\n--- Inventario ---")
            for p in self.productos.values():
                print(f"Código: {p.codigo} | Nombre: {p.nombre} | Cantidad: {p.cantidad} | Precio: {p.precio}")


# ------------------ Interfaz en Consola ------------------ #
def menu():
    inv = Inventario()

    while True:
        print("\n--- MENÚ INVENTARIO ---")
        print("1. Mostrar Inventario")
        print("2. Agregar Producto")
        print("3. Actualizar Producto")
        print("4. Eliminar Producto")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inv.mostrar_inventario()
        elif opcion == "2":
            codigo = input("Código: ")
            nombre = input("Nombre: ")
            try:
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                inv.agregar_producto(codigo, nombre, cantidad, precio)
            except ValueError:
                print("❌ Error: cantidad o precio inválidos.")
        elif opcion == "3":
            codigo = input("Código: ")
            try:
                cantidad = int(input("Nueva cantidad (o deje vacío): ") or -1)
                precio = float(input("Nuevo precio (o deje vacío): ") or -1)
                inv.actualizar_producto(
                    codigo,
                    cantidad if cantidad != -1 else None,
                    precio if precio != -1 else None,
                )
            except ValueError:
                print("❌ Error: entrada inválida.")
        elif opcion == "4":
            codigo = input("Código: ")
            inv.eliminar_producto(codigo)
        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    menu()
1