#!/usr/bin/env python3
"""
Sistema Avanzado de Gestión de Inventario (consola)
===================================================

Características principales:
- POO con clases `Producto` y `Inventario`.
- Uso de colecciones: diccionarios para acceso por ID, conjuntos para índices de nombre,
  listas/tuplas en operaciones de presentación.
- Persistencia en archivos: guardado/carga en JSON (serialización/deserialización).
- Menú de usuario en consola para gestionar el inventario.
- Código organizado y comentado para facilitar su comprensión.

Estructura de datos y decisiones de diseño
-----------------------------------------
- `Inventario` mantiene un diccionario principal `self._items: dict[str, Producto]` donde la clave
  es el ID único del producto. Esto permite acceso O(1) promedio por ID.
- Para búsquedas por nombre se emplea un índice `self._by_name: dict[str, set[str]]` que mapea
  el nombre normalizado (minúsculas y sin espacios extremos) al conjunto de IDs con ese nombre.
  Esto acelera la búsqueda exacta por nombre; las búsquedas por *subcadena* se resuelven
  recorriendo las claves del índice (aceptable en inventarios medianos y suficientemente rápido
  para una tarea académica), manteniendo la claridad del código.
- Persistencia en JSON: el formato almacena una lista de objetos con campos `id`, `nombre`,
  `cantidad`, `precio`. Se incluye manejo de errores y validación de esquema mínima.

Archivos generados
------------------
- `inventario.json`: archivo por defecto para guardar/cargar el inventario.

Cómo ejecutar
-------------
- Requisitos: Python 3.10+
- Ejecuta: `python inventario.py` (si guardas este archivo como `inventario.py`).

"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Set, List, Iterable, Optional, Tuple
import json
import os


# ==========================
#   MODELO DE DOMINIO
# ==========================

@dataclass(frozen=True)
class Producto:
    """Representa un producto del inventario.

    Campos:
      - id: str  (único)
      - nombre: str
      - cantidad: int  (>= 0)
      - precio: float  (>= 0)

    Se usa `frozen=True` para hacerlo inmutable; las "actualizaciones" se realizan creando
    una nueva instancia, lo que simplifica el control de integridad en `Inventario`.
    """
    id: str
    nombre: str
    cantidad: int
    precio: float

    def __post_init__(self) -> None:
        # Validación básica de datos
        if not self.id or not isinstance(self.id, str):
            raise ValueError("ID de producto inválido (debe ser cadena no vacía)")
        if not self.nombre or not isinstance(self.nombre, str):
            raise ValueError("Nombre de producto inválido (debe ser cadena no vacía)")
        if not isinstance(self.cantidad, int) or self.cantidad < 0:
            raise ValueError("Cantidad inválida (entero >= 0)")
        if not isinstance(self.precio, (int, float)) or self.precio < 0:
            raise ValueError("Precio inválido (número >= 0)")

    # Métodos "getters" implícitos por dataclass. Para setters, se crean nuevas instancias.
    def con_cantidad(self, nueva_cantidad: int) -> "Producto":
        return Producto(self.id, self.nombre, int(nueva_cantidad), self.precio)

    def con_precio(self, nuevo_precio: float) -> "Producto":
        return Producto(self.id, self.nombre, self.cantidad, float(nuevo_precio))

    def con_nombre(self, nuevo_nombre: str) -> "Producto":
        return Producto(self.id, nuevo_nombre, self.cantidad, self.precio)


# ==========================
#   REPOSITORIO/INVENTARIO
# ==========================

class Inventario:
    """Gestiona un conjunto de productos usando colecciones eficientes.

    - `_items`: dict[str, Producto]  (acceso O(1) por ID)
    - `_by_name`: dict[str, set[str]]  índice de nombre -> IDs
    """

    def __init__(self) -> None:
        self._items: Dict[str, Producto] = {}
        self._by_name: Dict[str, Set[str]] = {}

    # ---------- utilidades internas ----------
    @staticmethod
    def _norm_name(nombre: str) -> str:
        return nombre.strip().lower()

    def _index_add(self, p: Producto) -> None:
        key = self._norm_name(p.nombre)
        if key not in self._by_name:
            self._by_name[key] = set()
        self._by_name[key].add(p.id)

    def _index_remove(self, p: Producto) -> None:
        key = self._norm_name(p.nombre)
        ids = self._by_name.get(key)
        if ids:
            ids.discard(p.id)
            if not ids:
                self._by_name.pop(key, None)

    # ---------- operaciones públicas ----------
    def agregar(self, producto: Producto, *, sobrescribir: bool = False) -> None:
        """Agrega un producto nuevo.
        - Si `sobrescribir=False` (por defecto) y el ID ya existe -> ValueError.
        - Si `sobrescribir=True`, reemplaza el producto existente con el mismo ID.
        """
        existe = self._items.get(producto.id)
        if existe and not sobrescribir:
            raise ValueError(f"Ya existe un producto con ID '{producto.id}'.")
        if existe:
            # quitar índice previo
            self._index_remove(existe)
        self._items[producto.id] = producto
        self._index_add(producto)

    def eliminar(self, id_: str) -> Producto:
        p = self._items.pop(id_, None)
        if not p:
            raise KeyError(f"No existe producto con ID '{id_}'.")
        self._index_remove(p)
        return p

    def actualizar_cantidad(self, id_: str, nueva_cantidad: int) -> Producto:
        p = self.obtener_por_id(id_)
        actualizado = p.con_cantidad(nueva_cantidad)
        self._items[id_] = actualizado
        # nombre no cambia, índice intacto
        return actualizado

    def actualizar_precio(self, id_: str, nuevo_precio: float) -> Producto:
        p = self.obtener_por_id(id_)
        actualizado = p.con_precio(nuevo_precio)
        self._items[id_] = actualizado
        return actualizado

    def actualizar_nombre(self, id_: str, nuevo_nombre: str) -> Producto:
        p = self.obtener_por_id(id_)
        self._index_remove(p)
        actualizado = p.con_nombre(nuevo_nombre)
        self._items[id_] = actualizado
        self._index_add(actualizado)
        return actualizado

    def obtener_por_id(self, id_: str) -> Producto:
        p = self._items.get(id_)
        if not p:
            raise KeyError(f"No existe producto con ID '{id_}'.")
        return p

    def buscar_por_nombre(self, nombre: str, *, exacto: bool = False) -> List[Producto]:
        """Busca productos por nombre.
        - exacto=True: usa índice para coincidencia exacta (ignorando mayúsculas/minúsculas).
        - exacto=False: devuelve los que contengan la subcadena (case-insensitive).
        """
        q = self._norm_name(nombre)
        if exacto:
            ids = self._by_name.get(q, set())
            return [self._items[i] for i in ids]
        # Subcadena: recorrer claves y acumular
        resultados: List[Producto] = []
        for key, ids in self._by_name.items():
            if q in key:
                resultados.extend(self._items[i] for i in ids)
        # Ordenar de forma estable por nombre y luego ID para presentación
        resultados.sort(key=lambda p: (self._norm_name(p.nombre), p.id))
        return resultados

    def listar_todos(self) -> List[Producto]:
        return sorted(self._items.values(), key=lambda p: (self._norm_name(p.nombre), p.id))

    # ---------- persistencia ----------
    def guardar_en_json(self, ruta: str) -> None:
        data = [asdict(p) for p in self.listar_todos()]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def cargar_de_json(self, ruta: str, *, modo: str = "reemplazar") -> None:
        """Carga productos desde un archivo JSON.
        - modo="reemplazar": limpia el inventario antes de cargar.
        - modo="fusionar": inserta/actualiza por ID los productos del archivo.
        """
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Formato JSON inválido: se esperaba una lista de productos")
        if modo == "reemplazar":
            self._items.clear()
            self._by_name.clear()
        for obj in data:
            try:
                p = Producto(
                    id=str(obj["id"]),
                    nombre=str(obj["nombre"]),
                    cantidad=int(obj["cantidad"]),
                    precio=float(obj["precio"]),
                )
            except Exception as e:
                raise ValueError(f"Registro inválido en JSON: {obj!r} -> {e}")
            self.agregar(p, sobrescribir=True)


# ==========================
#   INTERFAZ DE CONSOLA
# ==========================

def _input_no_vacio(msg: str) -> str:
    while True:
        s = input(msg).strip()
        if s:
            return s
        print("✖ Entrada vacía. Intenta otra vez.")


def _input_entero_no_negativo(msg: str) -> int:
    while True:
        try:
            n = int(input(msg))
            if n < 0:
                raise ValueError
            return n
        except ValueError:
            print("✖ Ingresa un entero >= 0.")


def _input_flotante_no_negativo(msg: str) -> float:
    while True:
        try:
            x = float(input(msg))
            if x < 0:
                raise ValueError
            return x
        except ValueError:
            print("✖ Ingresa un número >= 0.")


def _imprimir_tabla(productos: Iterable[Producto]) -> None:
    filas: List[Tuple[str, str, str, str]] = []
    for p in productos:
        filas.append((p.id, p.nombre, str(p.cantidad), f"{p.precio:.2f}"))
    if not filas:
        print("(Sin resultados)")
        return
    # Calcular anchos de columnas
    headers = ("ID", "Nombre", "Cantidad", "Precio")
    cols = list(zip(*([headers] + filas)))  # transponer
    anchos = [max(len(x) for x in col) for col in cols]

    def fmt_row(row: Tuple[str, str, str, str]) -> str:
        return (
            row[0].ljust(anchos[0]) + "  " +
            row[1].ljust(anchos[1]) + "  " +
            row[2].rjust(anchos[2]) + "  " +
            row[3].rjust(anchos[3])
        )

    print(fmt_row(headers))
    print("-" * (sum(anchos) + 6))
    for fila in filas:
        print(fmt_row(fila))


def menu() -> None:
    inv = Inventario()
    ARCHIVO_DEFECTO = "inventario.json"

    # Carga opcional si existe el archivo
    if os.path.exists(ARCHIVO_DEFECTO):
        try:
            inv.cargar_de_json(ARCHIVO_DEFECTO, modo="reemplazar")
            print(f"✔ Inventario cargado desde '{ARCHIVO_DEFECTO}'.")
        except Exception as e:
            print(f"⚠ No se pudo cargar '{ARCHIVO_DEFECTO}': {e}")

    while True:
        print("\n=== MENÚ INVENTARIO ===")
        print("1) Añadir producto")
        print("2) Eliminar producto por ID")
        print("3) Actualizar cantidad")
        print("4) Actualizar precio")
        print("5) Actualizar nombre")
        print("6) Buscar por nombre (exacto)")
        print("7) Buscar por nombre (contiene)")
        print("8) Mostrar todos")
        print("9) Guardar a archivo JSON")
        print("10) Cargar desde archivo JSON")
        print("0) Salir (guardando)")

        opcion = _input_no_vacio("Elige una opción: ")

        try:
            if opcion == "1":
                id_ = _input_no_vacio("ID único: ")
                nombre = _input_no_vacio("Nombre: ")
                cantidad = _input_entero_no_negativo("Cantidad (>=0): ")
                precio = _input_flotante_no_negativo("Precio (>=0): ")
                inv.agregar(Producto(id_, nombre, cantidad, precio))
                print("✔ Producto añadido.")

            elif opcion == "2":
                id_ = _input_no_vacio("ID a eliminar: ")
                p = inv.eliminar(id_)
                print(f"✔ Eliminado: {p.id} - {p.nombre}")

            elif opcion == "3":
                id_ = _input_no_vacio("ID a actualizar cantidad: ")
                cantidad = _input_entero_no_negativo("Nueva cantidad: ")
                p = inv.actualizar_cantidad(id_, cantidad)
                print(f"✔ Nueva cantidad de {p.nombre}: {p.cantidad}")

            elif opcion == "4":
                id_ = _input_no_vacio("ID a actualizar precio: ")
                precio = _input_flotante_no_negativo("Nuevo precio: ")
                p = inv.actualizar_precio(id_, precio)
                print(f"✔ Nuevo precio de {p.nombre}: {p.precio:.2f}")

            elif opcion == "5":
                id_ = _input_no_vacio("ID a renombrar: ")
                nombre = _input_no_vacio("Nuevo nombre: ")
                p = inv.actualizar_nombre(id_, nombre)
                print(f"✔ ID {p.id} renombrado a: {p.nombre}")

            elif opcion == "6":
                nombre = _input_no_vacio("Nombre exacto a buscar: ")
                resultados = inv.buscar_por_nombre(nombre, exacto=True)
                _imprimir_tabla(resultados)

            elif opcion == "7":
                nombre = _input_no_vacio("Buscar nombre que contenga: ")
                resultados = inv.buscar_por_nombre(nombre, exacto=False)
                _imprimir_tabla(resultados)

            elif opcion == "8":
                _imprimir_tabla(inv.listar_todos())

            elif opcion == "9":
                ruta = input(f"Ruta de archivo [{ARCHIVO_DEFECTO}]: ").strip() or ARCHIVO_DEFECTO
                inv.guardar_en_json(ruta)
                print(f"✔ Guardado en '{ruta}'.")

            elif opcion == "10":
                ruta = input(f"Ruta de archivo [{ARCHIVO_DEFECTO}]: ").strip() or ARCHIVO_DEFECTO
                modo = input("Modo (reemplazar/fusionar) [reemplazar]: ").strip().lower() or "reemplazar"
                if modo not in {"reemplazar", "fusionar"}:
                    modo = "reemplazar"
                inv.cargar_de_json(ruta, modo=modo)
                print(f"✔ Cargado desde '{ruta}' (modo {modo}).")

            elif opcion == "0":
                try:
                    inv.guardar_en_json(ARCHIVO_DEFECTO)
                    print(f"✔ Inventario guardado automáticamente en '{ARCHIVO_DEFECTO}'. ¡Hasta luego!")
                except Exception as e:
                    print(f"⚠ No se pudo guardar automáticamente: {e}")
                break

            else:
                print("✖ Opción no válida. Intenta nuevamente.")

        except (ValueError, KeyError) as e:
            print(f"✖ Error: {e}")
        except FileNotFoundError:
            print("✖ Archivo no encontrado.")
        except json.JSONDecodeError as e:
            print(f"✖ Error de JSON: {e}")
        except Exception as e:
            print(f"✖ Error inesperado: {e}")


# Punto de entrada
if __name__ == "__main__":
    menu()
