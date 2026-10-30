import ast

from similares.serializacion import obtener_secuencia_funcion
from similares.similitud import (UMBRAL_DUPLICADO, similitud_jaccard, similitud_levenshtein)

def secuencia_de(codigo):
    arbol = ast.parse(codigo)
    funcion = arbol.body[0]
    return obtener_secuencia_funcion(funcion)

#TEST 1 POSITIVO: Variables renombradas
def test_variables_renombradas_OK():
    codigo_a = """
def suma_lista(numeros):
    total = 0
    for n in numeros:
        total += n
    return total
"""
    codigo_b = """
def sumar(valores):
    ac = 0
    for i in valores:
        ac += i
    return ac
"""
    score_J = similitud_jaccard(secuencia_de(codigo_a), secuencia_de(codigo_b))
    score_L = similitud_levenshtein(secuencia_de(codigo_a), secuencia_de(codigo_b))
    print("score Jaccard - Test 1:", score_J)
    print("score Levenshtein - Test 1:", score_L)
    assert score_J >= UMBRAL_DUPLICADO
    assert score_L >= UMBRAL_DUPLICADO

#TEST 2 POSITIVO: Lineas reordenadas
def test_lineas_reordenadas_OK():
    codigo_a = """
def promedio(numeros):
    total = 0
    cantidad = 0
    for n in numeros:
        total += n
        cantidad += 1
    return total / cantidad
"""
    codigo_b = """
def calcular_media(valores):
    cantidad = 0
    total = 0
    for v in valores:
        cantidad += 1
        total += v
    return total / cantidad
"""
    score_J = similitud_jaccard(secuencia_de(codigo_a), secuencia_de(codigo_b))
    score_L = similitud_levenshtein(secuencia_de(codigo_a), secuencia_de(codigo_b))
    print("score Jaccard - Test 2:", score_J)
    print("score Levenshtein - Test 2:", score_L)
    assert score_L >= UMBRAL_DUPLICADO

#TEST 3 NEGATIVO: Funciones diferentes 1
def test_funciones_distintas_1():
    codigo_a = """
def suma_lista(numeros):
    total = 0
    for n in numeros:
        total += n
    return total
"""
    codigo_b = """
def saludar(nombre):
    if nombre == "":
        print("Hola desconocido ;)")
    else:
        print("Hola " + nombre + ":D")
"""
    score = similitud_jaccard(secuencia_de(codigo_a), secuencia_de(codigo_b))
    print("score Jaccard - Test 3:", score)
    assert score < UMBRAL_DUPLICADO

#TEST 4 NEGATIVO: Funciones diferentes 2
def test_funciones_distintas_2():
    codigo_a = """
def procesar(datos):
    maximo = datos[0]   
    for n in datos:
        if n > maximo:
            maximo = n
    return maximo
"""
    codigo_b = """
def procesar(datos):
    resultado = []
    for apellido, nombre in datos:
        completo = apellido + ", " + nombre
        resultado.append(completo)
    return resultado
"""
    score = similitud_jaccard(secuencia_de(codigo_a), secuencia_de(codigo_b))
    print("score Jaccard - Test 4:", score)
    assert score < UMBRAL_DUPLICADO


# TEST 5 POSITIVO: Lineas reordenadas Desvio Estandar
def test_lineas_reordenadas_DesvEst_OK():
    codigo_a = """
def desvio_estandar(datos):
    n = len(datos)
    suma = 0
    suma_cuadrados = 0
    for x in datos:
        suma += x
        suma_cuadrados += x ** 2
    media = suma / n
    varianza = suma_cuadrados / n - media ** 2
    return varianza ** 0.5
"""
    codigo_b = """
def calcular_desvio(valores):
    n = len(valores)
    suma_cuadrados = 0
    suma = 0
    for v in valores:
        suma_cuadrados += v ** 2
        suma += v
    media = suma / n
    varianza = suma_cuadrados / n - media ** 2
    return varianza ** 0.5
"""
    score_J = similitud_jaccard(secuencia_de(codigo_a), secuencia_de(codigo_b))
    score_L = similitud_levenshtein(secuencia_de(codigo_a), secuencia_de(codigo_b))
    print("score Jaccard - Test 5:", score_J)
    print("score Levenshtein - Test 5:", score_L)
    assert score_J >= UMBRAL_DUPLICADO
    assert score_L >= UMBRAL_DUPLICADO

# TEST 6 NEGATIVO: Max común divisor (algoritmo de Euclides) vs búsqueda binaria.
def test_funciones_distintas_mcd_vs_busqBin():
    codigo_a = """
def mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
"""
    codigo_b = """
def busqueda_binaria(lista, objetivo):
    izq = 0
    der = len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            izq = medio + 1
        else:
            der = medio - 1
    return -1
"""
    score = similitud_jaccard(secuencia_de(codigo_a), secuencia_de(codigo_b))
    print("score Jaccard - Test 6:", score)
    assert score < UMBRAL_DUPLICADO