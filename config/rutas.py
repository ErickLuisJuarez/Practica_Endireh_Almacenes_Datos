from pathlib import Path

# Raíz del proyecto (dos niveles arriba de este archivo: config/rutas.py -> raíz)
RUTA_BASE = Path(__file__).resolve().parent.parent

RUTA_DATA = RUTA_BASE / "data"
RUTA_DATA_RAW = RUTA_DATA / "data-raw"
RUTA_DATA_PROCESSED = RUTA_DATA / "data-processed"
RUTA_DATA_INPUT_MODEL = RUTA_DATA / "data-input-model"
RUTA_DATA_MODEL = RUTA_DATA / "data-model"

# Nombre del archivo crudo del dataset, tal como fue entregado por la cátedra
ARCHIVO_ENDIREH_RAW = "Erick Luis Juárez - endireh_ml_dataset_texto_fecha.csv"
ARCHIVO_ENDIREH_PROCESSED = "endireh_2021_procesado.parquet"
