"""
Medidas de heterogeneidad/diversidad para variables cualitativas
"""
import polars as pl
import numpy as np


def obtener_proporciones(df: pl.DataFrame, columna: str) -> np.ndarray:
    """Devuelve el arreglo de proporciones p_i de cada categoría de columna, descartando nulos"""
    conteos = df[columna].drop_nulls().value_counts()["count"].to_numpy()
    return conteos / conteos.sum()


def calcular_gini_simpson(df: pl.DataFrame, columna: str) -> float:
    """
    Índice de Gini-Simpson
    """
    p = obtener_proporciones(df, columna)
    return float(1 - np.sum(p ** 2))


def calcular_iqv(df: pl.DataFrame, columna: str) -> float:
    """
    Índice de Variación Cualitativa. Normaliza Gini-Simpson al rango [0, 1] según el número de categorías k
    """
    p = obtener_proporciones(df, columna)
    k = len(p)
    if k <= 1:
        return 0.0
    gs = 1 - np.sum(p ** 2)
    return float(k * gs / (k - 1))


def calcular_entropia_shannon(df: pl.DataFrame, columna: str) -> dict:
    """
    Entropía de Shannon
    """
    p = obtener_proporciones(df, columna)
    k = len(p)
    p_positivas = p[p > 0]
    h = float(-np.sum(p_positivas * np.log2(p_positivas)))
    h_max = float(np.log2(k)) if k > 1 else 0.0
    return {
        "H": h,
        "H_max": h_max,
        "uniformidad_relativa": h / h_max if h_max > 0 else 0.0,
    }