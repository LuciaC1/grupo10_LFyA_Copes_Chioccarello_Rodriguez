from typing import List, Set, Tuple

UMBRAL_DUPLICADO: float = 0.75


def generar_ngramas(secuencia: List[str], n: int = 3) -> Set[Tuple[str, ...]]:
    if not secuencia:
        return set()
    if len(secuencia) < n:
        return {(tuple(secuencia), 0)}

    conteo = {}
    ngramas = set()
    for i in range(len(secuencia) - n + 1):
        grama = tuple(secuencia[i : i + n])
        ocurrencia = conteo.get(grama, 0)
        ngramas.add((grama, ocurrencia))
        conteo[grama] = ocurrencia + 1
    return ngramas


def similitud_jaccard(seq1: List[str], seq2: List[str], n: int = 3) -> float:
    if not seq1 and not seq2:
        return 1.0
    if not seq1 or not seq2:
        return 0.0

    ngramas1 = generar_ngramas(seq1, n)
    ngramas2 = generar_ngramas(seq2, n)

    interseccion = len(ngramas1.intersection(ngramas2))
    union = len(ngramas1.union(ngramas2))

    return interseccion / union if union > 0 else 0.0


def distancia_levenshtein(seq1: List[str], seq2: List[str]) -> int:
    filas = len(seq1) + 1
    columnas = len(seq2) + 1

    dp = [[0] * columnas for _ in range(filas)]

    for i in range(filas):
        dp[i][0] = i
    for j in range(columnas):
        dp[0][j] = j

    for i in range(1, filas):
        for j in range(1, columnas):
            costo = 0 if seq1[i - 1] == seq2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,          # Eliminación
                dp[i][j - 1] + 1,          # Inserción
                dp[i - 1][j - 1] + costo,  # Sustitución
            )
    return dp[-1][-1]


def similitud_levenshtein(seq1: List[str], seq2: List[str]) -> float:
    if not seq1 and not seq2:
        return 1.0
    max_len = max(len(seq1), len(seq2))
    if max_len == 0:
        return 1.0
    distancia = distancia_levenshtein(seq1, seq2)
    return 1.0 - (distancia / max_len)


def es_candidata_duplicado(score: float, umbral: float = UMBRAL_DUPLICADO) -> bool:
    return score >= umbral