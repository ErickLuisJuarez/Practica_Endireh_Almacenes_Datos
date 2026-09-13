# Proyecto ENDIREH 2021 — Violencia contra las Mujeres

## Objetivo
Analizar los microdatos de la Encuesta Nacional sobre la Dinámica de las Relaciones
en los Hogares (ENDIREH) 2021, del INEGI, aplicando una arquitectura de proyecto de
datos reproducible, un preprocesamiento riguroso (duplicados, tipos de datos,
imputación) y un análisis exploratorio con medidas de localización y variabilidad,
como paso previo a cualquier modelado.

Práctica 3 — Almacenes y Minería de Datos, Facultad de Ciencias, UNAM.

## Fuente de los datos
- Instituto Nacional de Estadística y Geografía (INEGI). *ENDIREH 2021*.
  https://www.inegi.org.mx/programas/endireh/2021/
- Se utiliza un archivo consolidado (`endireh_ml_dataset.csv`) provisto por la cátedra,
  con variables como `edad_primer_union`, `num_hijos`, `nivel_escolaridad`,
  `estado_civil_desc`, `sufrio_violencia_pareja`, `factor_expansion`, entre otras.
- El archivo original **no se sube al repositorio** por su tamaño; se coloca de forma
  local en `data/data-raw/`.

## Estructura del proyecto
```
proyecto-endireh-violencia/
├── config/                 # Rutas de archivos estáticos
├── data/
│   ├── data-raw/            # Datos originales, sin modificar (NO se versiona)
│   ├── data-processed/      # Datos limpios: sin duplicados, tipos corregidos, imputados
│   ├── data-input-model/    # Datos transformados, listos como entrada de un modelo
│   └── data-model/          # Salidas del modelo: predicciones, clusters, reglas
├── src/
│   ├── cleaning/             # Scripts de limpieza y preprocesamiento
│   ├── visualization/        # Scripts de gráficas y EDA
│   └── models/                # Scripts de entrenamiento y evaluación de modelos
├── notebooks/                # Notebooks exploratorios (no productivos)
├── README.md
└── requirements.txt
```

## Instalación del entorno
```bash
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Cómo ejecutar el pipeline
1. Colocar el archivo del dataset (sin modificar) en `data/data-raw/`.
2. Ajustar las rutas si es necesario en `config/rutas.py`.
3. Ejecutar el notebook de EDA en `notebooks/` o los scripts de `src/cleaning/`
   para generar los datos procesados en `data/data-processed/`.

## Framework de análisis de datos
Se utiliza **polars** (ver justificación completa en el reporte PDF), por su buen
desempeño frente a `pandas` en datasets medianos/grandes en una sola máquina,
manteniendo una sintaxis muy similar.

## Autor(es)
- Equipo: *(completar nombres del equipo)*
