"""
Medidas de concentración: coeficiente de Gini y curva de Lorenz.
"""
import numpy as np
import polars as pl


def calcular_gini(valores) -> float:
    """
    Coeficiente de Gini sobre un arreglo de valores no negativo
    """
    x = np.sort(np.asarray(valores, dtype=float))
    n = len(x)
    if n == 0 or x.sum() == 0:
        return 0.0
    indices = np.arange(1, n + 1)
    return float((2 * np.sum(indices * x) - (n + 1) * np.sum(x)) / (n * np.sum(x)))


def curva_lorenz(valores):
    """
    Calcula los puntos (x, y) de la curva de Lorenz para un arreglo de valores
    """
    x_sorted = np.sort(np.asarray(valores, dtype=float))
    n = len(x_sorted)
    y_acum = np.cumsum(x_sorted) / x_sorted.sum()
    x_acum = np.arange(1, n + 1) / n
    x_acum = np.insert(x_acum, 0, 0.0)
    y_acum = np.insert(y_acum, 0, 0.0)
    return x_acum, y_acum


def casos_violencia_por_entidad(
    df: pl.DataFrame,
    columna_violencia: str = "sufrio_violencia_pareja",
    columna_entidad: str = "nom_entidad",
    columna_peso: str = "factor_expansion",
) -> pl.DataFrame:
    """Agrega los casos de violencia por entidad, sumando el factor_expansion. Devuelve [columna_entidad, casos_ponderados] ordenado descendente"""
    return (
        df.filter(pl.col(columna_violencia) == True)
          .group_by(columna_entidad)
          .agg(pl.col(columna_peso).sum().alias("casos_ponderados"))
          .sort("casos_ponderados", descending=True)
    )