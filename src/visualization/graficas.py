"""
Funciones de graficación: boxplot de variabilidad, barras de heterogeneidad, curva de Lorenz y prevalencia por entidad
"""
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from src.models.concentracion import curva_lorenz, casos_violencia_por_entidad


def graficar_boxplot_variabilidad(df: pl.DataFrame, columnas: list[str], ruta_salida: str = None):
    """Boxplot comparando columnas numéricas entre el grupo con y sin violencia de pareja"""
    fig, axes = plt.subplots(1, len(columnas), figsize=(5.5 * len(columnas), 4.5))
    if len(columnas) == 1:
        axes = [axes]
    for ax, columna in zip(axes, columnas):
        datos_si = df.filter(pl.col("sufrio_violencia_pareja") == True)[columna].drop_nulls().to_numpy()
        datos_no = df.filter(pl.col("sufrio_violencia_pareja") == False)[columna].drop_nulls().to_numpy()
        ax.boxplot([datos_no, datos_si], tick_labels=["No sufrió", "Sufrió violencia"])
        ax.set_title(columna)
        ax.set_ylabel("valor")
    fig.suptitle("Dispersión por grupo de violencia de pareja")
    plt.tight_layout()
    if ruta_salida:
        plt.savefig(ruta_salida, dpi=120)
    return fig


def graficar_barras_heterogeneidad(df: pl.DataFrame, columna: str, ruta_salida: str = None):
    """Barras de frecuencia de las categorías de una variable cualitativa"""
    conteo = df[columna].value_counts().sort(columna)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(conteo[columna].to_list(), conteo["count"].to_list(), color="#4C72B0")
    ax.set_title(f"Distribución de {columna}")
    ax.set_xlabel(columna)
    ax.set_ylabel("Número de mujeres")
    plt.tight_layout()
    if ruta_salida:
        plt.savefig(ruta_salida, dpi=120)
    return fig


def graficar_curva_lorenz(valores, gini: float, titulo: str = "Curva de Lorenz", color: str = "#C44E52", ruta_salida: str = None):
    """Curva de Lorenz con la diagonal de igualdad perfecta, sombreada"""
    x, y = curva_lorenz(valores)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y, marker="o", markersize=3, color=color, label="Curva de Lorenz")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Igualdad perfecta")
    ax.fill_between(x, y, x, alpha=0.15, color=color)
    ax.set_xlabel("Proporción acumulada de unidades")
    ax.set_ylabel("Proporción acumulada del total")
    ax.set_title(f"{titulo} — Gini = {gini:.4f}")
    ax.legend()
    ax.set_aspect("equal")
    plt.tight_layout()
    if ruta_salida:
        plt.savefig(ruta_salida, dpi=120)
    return fig


def graficar_prevalencia_entidad(df_casos: pl.DataFrame, ruta_salida: str = None):
    """Barras horizontales de casos de violencia de pareja por entidad, ponderados. Recibe el DataFrame ya agregado (ver casos_violencia_por_entidad)"""
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(df_casos["nom_entidad"], df_casos["casos_ponderados"], color="#C44E52")
    ax.set_xlabel("Casos de violencia de pareja estimados (ponderados)")
    ax.set_title("Prevalencia estimada de violencia de pareja por entidad")
    ax.invert_yaxis()
    plt.tight_layout()
    if ruta_salida:
        plt.savefig(ruta_salida, dpi=120)
    return fig