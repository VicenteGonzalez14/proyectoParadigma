import json
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "poker_dataset.json"

def cargar_dataset():
    """Carga el dataset desde poker_dataset.json y devuelve un DataFrame."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {DATA_PATH}")
    
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convertir a DataFrame plano (solo info principal de cada mano)
    df = pd.json_normalize(data)

    # Validación básica
    print(f"✅ Dataset cargado correctamente: {len(df)} manos encontradas.")
    print(f"📊 Columnas disponibles: {list(df.columns)}")
    
    return df