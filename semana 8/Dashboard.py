import os

# Lista para almacenar el historial de scripts vistos
historial = []

def mostrar_codigo(ruta_script):
    """
    Muestra el contenido de un archivo dado su path.
    """
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            print(f"\n📄 --- Código de {ruta_script} ---\n")
            print(archivo.read())
            historial.append(ruta_script)  # Guarda en historial
    except FileNotFoundError:
        print("❌ El archivo no se encontró.")
    except Exception as e:
        print(f"⚠️ Ocurrió un error al leer el archivo: {e}")


def mostrar_historial():
    """
    Muestra la lista de archivos que el usuario ha consultado.
    """
    print("\n📚 Historial de archivos visualizados:")
    if not historial:
        print("No has consultado ningún archivo todavía.")
    else:
        for i, archivo in enumerate(historial, start=1):
            print(f"{i}. {archivo}")


def mostrar_menu():
    """
    Muestra el menú principal y permite al usuario seleccionar scripts para ver su código.
    """
    ruta_base = os.path.dirname(__file__)

    # Diccionario de opciones con rutas relativas
    opciones = {
        '1': 'UNIDAD 1/1.2. Tecnicas de Programacion/1.2.1. Ejemplo Tecnicas de Programacion.py',
        '2': 'UNIDAD 1/1.3. Estructuras Condicionales/condicionales.py',
        '3': 'UNIDAD 2/2.1. POO/ejemplo_clases.py',
        '4': 'UNIDAD 2/2.2. Herencia/herencia_basica.py'
        # Puedes agregar más scripts aquí
    }

    while True:
        print("\n🧠 Panel de Gestión de POO - Dashboard")
        print("-------------------------------------")
        for key in opciones:
            print(f"{key} - Ver {os.path.basename(opciones[key])}")
        print("9 - Ver historial de archivos consultados")
        print("0 - Salir")

        eleccion = input("📌 Elige una opción: ")
        if eleccion == '0':
            print("👋 Saliendo del dashboard. ¡Hasta pronto!")
            break
        elif eleccion == '9':
            mostrar_historial()
        elif eleccion in opciones:
            ruta_script = os.path.join(ruta_base, opciones[eleccion])
            mostrar_codigo(ruta_script)
        else:
            print("⚠️ Opción no válida. Intenta nuevamente.")

# Punto de entrada del programa
if __name__ == "__main__":
    mostrar_menu()
