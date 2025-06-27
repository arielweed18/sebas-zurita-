# Programa: Cálculo del área de un triángulo


def calcular_area_triangulo(base: float, altura: float) -> float:
    """
    Calcula el área de un triángulo a partir de la base y la altura dadas.
    :param base: Base del triángulo (float)
    :param altura: Altura del triángulo (float)
    :return: Área calculada (float)
    """
    area = (base * altura) / 2
    return area

# Solicita datos al usuario
nombre_usuario = input("Ingrese su nombre: ")  # string
print(f"Hola, {nombre_usuario}. Vamos a calcular el área de un triángulo.")

base_triangulo = float(input("Ingrese la base del triángulo en cm: "))  # float
altura_triangulo = float(input("Ingrese la altura del triángulo en cm: "))  # float

# Cálculo del área
area_resultado = calcular_area_triangulo(base_triangulo, altura_triangulo)

# Evaluación con tipo booleano
area_grande = area_resultado > 50  # boolean

# Resultados
print(f"\nEl área del triángulo es: {area_resultado:.2f} cm²")
print(f"¿El área es mayor a 50 cm²?: {area_grande}")
