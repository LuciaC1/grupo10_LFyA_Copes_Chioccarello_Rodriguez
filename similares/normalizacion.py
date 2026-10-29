import ast
import builtins
import copy
from typing import Dict, List

NOMBRES_BUILTINS = set(dir(builtins))


class NormalizadorAST(ast.NodeTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.mapa_variables: Dict[str, str] = {}
        self.contador_vars: int = 0

    def _obtener_token_variable(self, nombre: str) -> str:
        if nombre not in self.mapa_variables:
            self.contador_vars += 1
            self.mapa_variables[nombre] = f"VAR{self.contador_vars}"
        return self.mapa_variables[nombre]

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        node.name = "FUNC"
        node.returns = None
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        node.name = "FUNC"
        node.returns = None
        return self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> ast.AST:
        node.arg = self._obtener_token_variable(node.arg)
        node.annotation = None
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id not in NOMBRES_BUILTINS:
            node.id = self._obtener_token_variable(node.id)
        return self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        node.value = "LIT"
        return node


def normalizar_ast(nodo_funcion: ast.AST) -> ast.AST:
    copia_arbol = copy.deepcopy(nodo_funcion)
    normalizador = NormalizadorAST()
    return normalizador.visit(copia_arbol)