import ast
import os
from dataclasses import dataclass
from typing import List


@dataclass
class FuncionExtraida:
    nombre: str
    archivo: str
    linea: int
    nodo_ast: ast.AST

    @property
    def identificador(self) -> str:
        nombre_archivo = os.path.basename(self.archivo)
        return f"{nombre_archivo}:{self.nombre}"


def extraer_funciones_archivo(ruta_archivo: str) -> List[FuncionExtraida]:
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    try:
        arbol = ast.parse(codigo, filename=ruta_archivo)
    except SyntaxError as e:
        print(f"[ADVERTENCIA] Error de sintaxis en {ruta_archivo}: {e}")
        return []

    funciones: List[FuncionExtraida] = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funciones.append(
                FuncionExtraida(
                    nombre=nodo.name,
                    archivo=ruta_archivo,
                    linea=nodo.lineno,
                    nodo_ast=nodo,
                )
            )
    return funciones


def extraer_funciones_directorio(directorio: str) -> List[FuncionExtraida]:
    todas_las_funciones: List[FuncionExtraida] = []
    for raiz, _, archivos in os.walk(directorio):
        for archivo in sorted(archivos):
            if archivo.endswith(".py"):
                ruta_completa = os.path.join(raiz, archivo)
                todas_las_funciones.extend(extraer_funciones_archivo(ruta_completa))
    return todas_las_funciones