"""
Funciones de visualización para el EDA del dataset ENDIREH 2021.
Extraídas del notebook notebooks/endireh_practica3.ipynb.
"""
import polars as pl
import matplotlib.pyplot as plt


def boxplot_por_violencia(df: pl.DataFrame, columnas: list[str], ruta_salida: str = None):
    """
    Genera un boxplot comparando la dispersión de una o más columnas
    numéricas entre el grupo que reportó violencia de pareja y el que no.
    """
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
