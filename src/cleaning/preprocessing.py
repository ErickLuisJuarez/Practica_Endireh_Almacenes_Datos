import polars as pl

def eliminar_duplicados(df: pl.DataFrame) -> pl.DataFrame:
    """Elimina filas duplicadas exactas."""
    return df.unique(keep="first", maintain_order=True)

def limpiar_valores_centinela(df: pl.DataFrame) -> pl.DataFrame:
    """
    Recodifica valores centinela/códigos especiales del INEGI a nulos (None).
    Para edad_primer_union también se descartan edades no plausibles (< 12 años),
    criterio mínimo de nupcialidad usado en estudios de ENDIREH.
    """
    return df.with_columns([
        pl.when(
            pl.col("edad_primer_union").is_in([98, 99])
            | (pl.col("edad_primer_union") < 12)
        )
          .then(None)
          .otherwise(pl.col("edad_primer_union"))
          .alias("edad_primer_union"),

        pl.when(pl.col("ingreso_pareja").is_in([999997, 999998, 999999]))
          .then(None)
          .otherwise(pl.col("ingreso_pareja"))
          .alias("ingreso_pareja"),
    ])

def convertir_tipos_datos(df: pl.DataFrame) -> pl.DataFrame:
    """Aplica el tipado adecuado a columnas categóricas, ordinales y booleanas."""
    orden_escolaridad = ["A1", "A2", "B1", "B2", "C1", "C2"]
    columnas_id_categoricas = [
        "cve_entidad", "cve_municipio", "estado_civil_id", "pareja_trabaja_id",
        "dinero_propio_id", "apoyo_gobierno_id", "tiene_ahorros_id",
        "propietaria_vivienda_id",
    ]
    
    return df.with_columns([
        *[pl.col(c).cast(pl.Utf8).cast(pl.Categorical) for c in columnas_id_categoricas],
        pl.col("nivel_escolaridad").cast(pl.Enum(orden_escolaridad)),
        pl.col("sufrio_violencia_pareja").cast(pl.Boolean),
        pl.col("nom_entidad").cast(pl.Categorical),
        pl.col("nom_municipio").cast(pl.Categorical),
        pl.col("estado_civil_desc").cast(pl.Categorical),
    ])

def imputar_datos(df: pl.DataFrame) -> pl.DataFrame:
    """
    Imputa lógicamente los datos faltantes.
    Para `ingreso_pareja`, asigna 0.0 cuando la pareja no trabaja.
    """
    return df.with_columns([
        pl.when(pl.col("pareja_trabaja_desc") == "No")
          .then(0.0)
          .otherwise(pl.col("ingreso_pareja"))
          .alias("ingreso_pareja"),
    ])

def pipeline_limpieza_completo(df: pl.DataFrame) -> pl.DataFrame:
    """Ejecuta el pipeline completo de preprocesamiento."""
    df_clean = eliminar_duplicados(df)
    df_clean = limpiar_valores_centinela(df_clean)
    df_clean = convertir_tipos_datos(df_clean)
    df_clean = imputar_datos(df_clean)
    return df_clean