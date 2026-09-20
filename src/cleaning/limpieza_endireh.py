"""
Funciones de limpieza y preprocesamiento del dataset ENDIREH 2021.
"""
import polars as pl


def eliminar_duplicados(df: pl.DataFrame) -> pl.DataFrame:
    """Elimina filas exactamente duplicadas."""
    return df.unique(keep="first")


def limpiar_codigos_centinela(df: pl.DataFrame) -> pl.DataFrame:
    """Recodifica como nulos los códigos 'no sabe/no aplica' e inconsistencias (<=0) del INEGI."""
    return df.with_columns([
        pl.when(pl.col("edad_primer_union").is_in([98, 99]) | (pl.col("edad_primer_union") <= 0))
          .then(None)
          .otherwise(pl.col("edad_primer_union"))
          .alias("edad_primer_union"),
        pl.when(pl.col("ingreso_pareja").is_in([999997, 999998, 999999]))
          .then(None)
          .otherwise(pl.col("ingreso_pareja"))
          .alias("ingreso_pareja"),
    ])


def imputar_ingreso_pareja(df: pl.DataFrame) -> pl.DataFrame:
    """Imputa ingreso_pareja con 0 cuando la pareja no trabaja (cero estructural)."""
    return df.with_columns([
        pl.when(pl.col("pareja_trabaja_desc") == "No")
          .then(0.0)
          .otherwise(pl.col("ingreso_pareja"))
          .alias("ingreso_pareja"),
    ])
