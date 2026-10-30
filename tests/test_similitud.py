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
    score_L = similitud_levenshtein(secuencia_de(codigo_a), secuencia_de(codigo_b))
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
    assert score < UMBRAL_DUPLICADO