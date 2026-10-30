import argparse
import os
import sys  
from typing import List, Tuple

from similares.extraccion import FuncionExtraida, extraer_funciones_directorio
from similares.serializacion import obtener_secuencia_funcion
from similares.similitud import (
    UMBRAL_DUPLICADO,
    es_candidata_duplicado,
    similitud_jaccard,
    similitud_levenshtein,
)


def buscar_funcion_objetivo(
    funciones: List[FuncionExtraida], especificacion: str
) -> FuncionExtraida:
    """Busca la función objetivo a partir del formato 'archivo.py:nombre_funcion'."""
    if ":" not in especificacion:
        raise ValueError(
            "El formato de --funcion debe ser 'archivo.py:mi_funcion'"
        )

    archivo_buscado, nombre_buscado = especificacion.split(":", 1)
    nombre_base_buscado = os.path.basename(archivo_buscado)

    for func in funciones:
        mismo_nombre = func.nombre == nombre_buscado
        mismo_archivo = (
            os.path.basename(func.archivo) == nombre_base_buscado
            or func.archivo.endswith(archivo_buscado)
        )
        if mismo_nombre and mismo_archivo:
            return func

    raise LookupError(
        f"No se encontró la función '{nombre_buscado}' en el archivo '{archivo_buscado}'."
    )


def ranking_similares(
    objetivo: FuncionExtraida,
    universo: List[FuncionExtraida],
    metrica: str = "jaccard",
    n_gramas: int = 3,
    top_k: int = 5,
) -> List[Tuple[FuncionExtraida, float]]:
    """Compara la función objetivo contra todas las demás y devuelve el top-K."""
    seq_objetivo = obtener_secuencia_funcion(objetivo.nodo_ast)
    resultados: List[Tuple[FuncionExtraida, float]] = []

    for candidata in universo:
        # Excluir exactamente la misma función en la misma línea y archivo
        if (
            candidata.archivo == objetivo.archivo
            and candidata.nombre == objetivo.nombre
            and candidata.linea == objetivo.linea
        ):
            continue

        seq_candidata = obtener_secuencia_funcion(candidata.nodo_ast)

        if metrica == "jaccard":
            score = similitud_jaccard(seq_objetivo, seq_candidata, n=n_gramas)
        elif metrica == "levenshtein":
            score = similitud_levenshtein(seq_objetivo, seq_candidata)
        else:
            score_j = similitud_jaccard(seq_objetivo, seq_candidata, n=n_gramas)
            score_l = similitud_levenshtein(seq_objetivo, seq_candidata)
            score = (score_j + score_l) / 2.0

        resultados.append((candidata, score))

    resultados.sort(key=lambda item: item[1], reverse=True)
    return resultados[:top_k]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Motor de búsqueda de funciones similares vía AST."
    )
    parser.add_argument(
        "--dir",
        required=True,
        help="Directorio raíz del repositorio Python a analizar.",
    )
    parser.add_argument(
        "--funcion",
        required=True,
        help="Función objetivo en formato 'archivo.py:nombre_funcion'.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Cantidad de funciones más similares a devolver (por defecto: 5).",
    )
    parser.add_argument(
        "--metrica",
        choices=["jaccard", "levenshtein", "promedio"],
        default="jaccard",
        help="Métrica de similitud a utilizar (por defecto: jaccard).",
    )
    parser.add_argument(
        "--ngramas",
        type=int,
        default=3,
        help="Tamaño de n para n-gramas en Jaccard (por defecto: 3).",
    )
    parser.add_argument(
        "--umbral",
        type=float,
        default=UMBRAL_DUPLICADO,
        help=f"Umbral para considerar duplicado (por defecto: {UMBRAL_DUPLICADO}).",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"[ERROR] El directorio '{args.dir}' no existe.", file=sys.stderr)
        sys.exit(1)

    funciones = extraer_funciones_directorio(args.dir)
    if not funciones:
        print(f"[ERROR] No se encontraron funciones en '{args.dir}'.", file=sys.stderr)
        sys.exit(1)

    try:
        objetivo = buscar_funcion_objetivo(funciones, args.funcion)
    except (ValueError, LookupError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    top_similares = ranking_similares(
        objetivo=objetivo,
        universo=funciones,
        metrica=args.metrica,
        n_gramas=args.ngramas,
        top_k=args.top,
    )

    print("=" * 75)
    print(f"FUNCIÓN OBJETIVO : {objetivo.identificador} (Línea {objetivo.linea})")
    print(f"MÉTRICA          : {args.metrica.upper()} | UMBRAL DUPLICADO: {args.umbral:.2f}")
    print("=" * 75)
    print(f"{'#':<3} {'FUNCIÓN':<32} {'UBICACIÓN':<22} {'SCORE':<8} {'ESTADO'}")
    print("-" * 75)

    for idx, (func, score) in enumerate(top_similares, start=1):
        estado = (
            "CANDIDATA A DUPLICADO"
            if es_candidata_duplicado(score, args.umbral)
            else "Distinta"
        )
        ubicacion = f"{os.path.basename(func.archivo)}:{func.linea}"
        print(f"{idx:<3} {func.nombre:<32} {ubicacion:<22} {score:<8.4f} {estado}")
    print("=" * 75)


if __name__ == "__main__":
    main()