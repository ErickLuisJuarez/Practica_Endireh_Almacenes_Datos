import polars as pl
import numpy as np

def obtener_resumen_nulos(df: pl.DataFrame) -> pl.DataFrame:
    """Genera una tabla con el conteo y porcentaje de nulos por columna."""
    nulos = df.null_count()
    n_filas = df.shape[0]
    return pl.DataFrame({
        "columna": df.columns,
        "nulos": [int(nulos[c][0]) for c in df.columns],
        "pct_nulos": [round(100 * int(nulos[c][0]) / n_filas, 1) for c in df.columns],
    }).filter(pl.col("nulos") > 0).sort("nulos", descending=True)

def calcular_medidas_localizacion(df: pl.DataFrame) -> pl.DataFrame:
    """Calcula medidas de tendencia central y cuantiles."""
    return df.select([
        pl.col("edad_primer_union").mean().alias("media_edad_union"),
        pl.col("edad_primer_union").median().alias("mediana_edad_union"),
        pl.col("edad_primer_union").mode().first().alias("moda_edad_union"),
        pl.col("edad_primer_union").quantile(0.10).alias("P10_edad_union"),
        pl.col("edad_primer_union").quantile(0.25).alias("Q1_edad_union"),
        pl.col("edad_primer_union").quantile(0.75).alias("Q3_edad_union"),
        pl.col("edad_primer_union").quantile(0.90).alias("P90_edad_union"),
        pl.col("edad_primer_union").count().alias("n_no_nulo_edad_union"),

        pl.col("num_hijos").mean().alias("media_num_hijos"),
        pl.col("num_hijos").median().alias("mediana_num_hijos"),
        pl.col("num_hijos").mode().first().alias("moda_num_hijos"),
        pl.col("num_hijos").quantile(0.25).alias("Q1_num_hijos"),
        pl.col("num_hijos").quantile(0.75).alias("Q3_num_hijos"),
        pl.col("num_hijos").count().alias("n_no_nulo_num_hijos"),
    ])

def calcular_medidas_variabilidad(df: pl.DataFrame, columna: str, grupo_label: str) -> dict:
    """Calcula el rango, varianza, desviación estándar, CV y IQR para una columna."""
    serie = df[columna].drop_nulls()
    if serie.len() == 0:
        return None
    rango = serie.max() - serie.min()
    varianza = serie.var()
    desv_std = serie.std()
    media = serie.mean()
    cv = (desv_std / media * 100) if media not in (0, None) else None
    q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
    iqr = q3 - q1
    return {
        "variable": columna,
        "grupo": grupo_label,
        "n": serie.len(),
        "rango": rango,
        "varianza": varianza,
        "desv_std": desv_std,
        "CV_%": cv,
        "IQR": iqr
    }

def calcular_media_ponderada(df: pl.DataFrame, columna: str, columna_peso: str = "factor_expansion") -> float:
    """
    Calcula la media ponderada de columna usando columna_peso filtrando nulos de columna antes del cálculo
    """
    df_valido = df.drop_nulls(subset=[columna])
    valores = df_valido[columna].to_numpy()
    pesos = df_valido[columna_peso].to_numpy()
    return float(np.average(valores, weights=pesos))

def calcular_mediana_ponderada(df: pl.DataFrame, columna: str, columna_peso: str = "factor_expansion") -> float:
    """
    Calcula la mediana ponderada de columna usando columna_peso
    """
    df_valido = df.drop_nulls(subset=[columna]).sort(columna)
    valores = df_valido[columna].to_numpy()
    pesos = df_valido[columna_peso].to_numpy()
    acumulado = np.cumsum(pesos)
    mitad = acumulado[-1] / 2
    idx = np.searchsorted(acumulado, mitad)
    return float(valores[idx])