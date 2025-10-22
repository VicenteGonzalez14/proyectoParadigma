import pandas as pd
from .process import cargar_dataset

def calcular_estadisticas_basicas():
    """Calcula estadísticas simples del dataset cargado."""
    df = cargar_dataset()

    total_manos = len(df)
    total_ganadas = (df["resultado_usuario"] == "gano").sum()
    total_perdidas = (df["resultado_usuario"] == "perdio").sum()
    tasa_victoria = round(total_ganadas / total_manos * 100, 2) if total_manos > 0 else 0

    bote_promedio = round(df["bote_final"].mean(), 2) if "bote_final" in df.columns else 0
    agresividad_media = round(df["puntos_estrategia.agresividad"].mean(), 2)
    riesgo_medio = round(df["puntos_estrategia.riesgo"].mean(), 2)

    resumen = {
        "total_manos": int(total_manos),
        "ganadas": int(total_ganadas),
        "perdidas": int(total_perdidas),
        "tasa_victoria": tasa_victoria,
        "bote_promedio": bote_promedio,
        "agresividad_media": agresividad_media,
        "riesgo_medio": riesgo_medio
    }

    print("📈 Estadísticas básicas calculadas:")
    for k, v in resumen.items():
        print(f" - {k}: {v}")

    return resumen
