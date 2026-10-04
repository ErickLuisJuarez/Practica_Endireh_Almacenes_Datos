# Proyecto ENDIREH 2021 — Violencia contra las Mujeres

## Objetivo
Analizar los microdatos de la Encuesta Nacional sobre la Dinámica de las Relaciones
en los Hogares (ENDIREH) 2021, del INEGI, aplicando una arquitectura de proyecto de
datos reproducible, un preprocesamiento riguroso (eliminación de duplicados, corrección
de tipos de datos e imputación de valores centinela) y un análisis exploratorio con
medidas de localización, variabilidad, heterogeneidad cualitativa y concentración territorial,
como paso previo a cualquier modelado.

- **Práctica 3:** Almacenes y Minería de Datos, Facultad de Ciencias, UNAM.
- **Práctica 4:** Almacenes y Minería de Datos, Facultad de Ciencias, UNAM.

## Fuente de los datos
- Instituto Nacional de Estadística y Geografía (INEGI). *ENDIREH 2021*.
  https://www.inegi.org.mx/programas/endireh/2021/
- Se utiliza un archivo consolidado (`Erick Luis Juárez - endireh_ml_dataset_texto_fecha.csv`)
  provisto por la cátedra, con variables como `edad_primer_union`, `num_hijos`,
  `nivel_escolaridad`, `estado_civil_desc`, `sufrio_violencia_pareja`, `ingreso_pareja`,
  `factor_expansion`, entre otras.
- El archivo original **no se sube al repositorio** por su tamaño; se coloca de forma
  local en `data/data-raw/`.

## Estructura del proyecto
```text
proyecto-endireh-violencia/
├── config/                 # Rutas de archivos estáticos
├── data/
│   ├── data-raw/           # Datos originales, sin modificar (NO se versiona)
│   ├── data-processed/     # Datos limpios: sin duplicados, tipos corregidos, imputados
│   ├── data-input-model/   # Datos transformados, listos como entrada de un modelo
│   └── data-model/         # Salidas del modelo: predicciones, clusters, reglas
├── src/
│   ├── cleaning/           # Scripts de limpieza y preprocesamiento
│   ├── metrics/            # Funciones puras (Heterogeneidad, Gini, Lorenz)
│   ├── visualization/      # Scripts de gráficas y EDA
│   └── models/             # Scripts de entrenamiento y evaluación de modelos
├── notebooks/              # Notebooks exploratorios (no productivos)
│   ├── endireh_practica3.ipynb
│   ├── medidas_localizacion.ipynb
│   ├── medidas_variabilidad.ipynb
│   ├── medidas_heterogeneidad.ipynb
│   ├── medidas_concentracion.ipynb
│   └── comparacion_gini_entropia.ipynb
├── reports/                # Reportes de salida y figuras generadas
│   └── figures/
├── README.md
```

## Alcance y Descripción de las Prácticas

### Práctica 3 — Preprocesamiento y Limpieza de Datos

* **Eliminación de duplicados:** Identificación y remoción de registros idénticos en el dataset.
* **Corrección de tipos de datos y codificación:** Manejo de codificación UTF-8 y estandarización de columnas numéricas y categóricas.
* **Manejo de valores centinela del INEGI:** Tratamiento y filtrado de códigos de no respuesta (`98`, `99`, `999998`).
* **Generación del dataset procesado:** Creación del archivo consolidado `data/data-processed/endireh_2021_limpio.csv`.

### Práctica 4 — Análisis Exploratorio de Datos (EDA)

* **Medidas de Localización y Variabilidad:** Cálculo de media, mediana ponderada (por `factor_expansion`), rango intercuartílico (IQR) y coeficiente de variación (CV) en variables continuas y discretas.
* **Medidas de Heterogeneidad Cualitativa:** Evaluación de la diversidad y dispersión en variables categóricas (`nivel_escolaridad`, `estado_civil_desc`, `sufrio_violencia_pareja`) utilizando la Entropía de Shannon, el Índice de Gini-Simpson y el Índice de Variación Cualitativa (IQV).
* **Medidas de Concentración Territorial:** Análisis de la distribución geográfica estatal de los casos de violencia mediante la construcción de la Curva de Lorenz y el cálculo del Coeficiente de Gini.

## Instalación del entorno

```bash
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Cómo ejecutar el pipeline

1. Colocar el archivo del dataset (sin modificar) en `data/data-raw/`.
2. Ajustar o verificar las rutas ejecutando `python config/rutas.py`.
3. Ejecutar los notebooks de EDA en `notebooks/` o los scripts de `src/cleaning/`
para generar los datos procesados en `data/data-processed/endireh_2021_limpio.csv`.

## Framework de análisis de datos

Se utiliza **polars** (ver justificación completa en el reporte PDF), por su buen
desempeño frente a `pandas` en datasets medianos/grandes en una sola máquina,
manteniendo una sintaxis muy similar.

## Autor(es)

* Equipo: Erick Luis Juárez
Julio Alejandro Herrera Avalos
Luis Mario Solares Ramos
Cesar Candelario Fuentes Anica