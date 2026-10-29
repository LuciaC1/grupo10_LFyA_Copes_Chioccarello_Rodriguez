import ast
from typing import List

from normalizacion import normalizar_ast


def serializar_preorder(nodo: ast.AST) -> List[str]:
    secuencia: List[str] = []

    def _recorrer(actual: ast.AST) -> None:
        if isinstance(actual, ast.expr_context):
            return

        tipo_nodo = type(actual).__name__
        secuencia.append(tipo_nodo)

        if isinstance(actual, ast.arg):
            secuencia.append(actual.arg)
        elif isinstance(actual, ast.Name):
            secuencia.append(actual.id)
        elif isinstance(actual, ast.Constant):
            secuencia.append(str(actual.value))

        for hijo in ast.iter_child_nodes(actual):
            _recorrer(hijo)

    _recorrer(nodo)
    return secuencia


def obtener_secuencia_funcion(nodo_funcion: ast.AST) -> List[str]:
    arbol_normalizado = normalizar_ast(nodo_funcion)
    return serializar_preorder(arbol_normalizado)