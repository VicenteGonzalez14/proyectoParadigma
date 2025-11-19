import pandas as pd
import numpy as np
from collections import Counter
from .process import cargar_dataset

POSICIONES_ORDEN = ["UTG", "UTG+1", "MP", "LJ", "HJ", "CO", "BTN", "SB", "BB"]


# =====================================================
# 1. ESTADÍSTICAS GENERALES
# =====================================================
def estadisticas_generales():
    df = cargar_dataset()

    if df.empty:
        return {
            "total_manos": 0,
            "ganadas": 0,
            "perdidas": 0,
            "tasa_victoria": 0.0,
            "bote_promedio": 0.0,
            "agresividad_media": 0.0,
            "riesgo_medio": 0.0,
            "total_ganado": 0,
            "total_perdido": 0,
            "profit_neto": 0,
            "promedio_ganado": 0,
            "promedio_perdido": 0
        }

    total_manos = len(df)
    total_ganadas = (df["resultado_usuario"] == "gano").sum()
    total_perdidas = (df["resultado_usuario"] == "perdio").sum()

    tasa_victoria = round(total_ganadas / total_manos * 100, 2)

    bote_promedio = round(df["bote_final"].mean(), 2)

    # COLUMNA CORRECTA DESDE JSON NORMALIZADO
    agresividad_media = round(df["puntos_estrategia.agresividad"].mean(), 3)
    riesgo_medio      = round(df["puntos_estrategia.riesgo"].mean(), 3)

    ganancias = df["ganancia_usuario"]
    total_ganado = ganancias[ganancias > 0].sum()
    total_perdido = -ganancias[ganancias < 0].sum()
    profit_neto = total_ganado - total_perdido

    promedio_ganado = round(ganancias[ganancias > 0].mean(), 2) if (ganancias > 0).any() else 0
    promedio_perdido = round((-ganancias[ganancias < 0]).mean(), 2) if (ganancias < 0).any() else 0

    return {
        "total_manos": int(total_manos),
        "ganadas": int(total_ganadas),
        "perdidas": int(total_perdidas),
        "tasa_victoria": tasa_victoria,
        "bote_promedio": bote_promedio,
        "agresividad_media": agresividad_media,
        "riesgo_medio": riesgo_medio,
        "total_ganado": int(total_ganado),
        "total_perdido": int(total_perdido),
        "profit_neto": int(profit_neto),
        "promedio_ganado": promedio_ganado,
        "promedio_perdido": promedio_perdido
    }

def calcular_estadisticas_basicas():
    return estadisticas_generales()


# =====================================================
# 2. WINRATE POR POSICIÓN
# =====================================================
def winrate_por_posicion():
    df = cargar_dataset()
    if df.empty:
        return []

    df["victoria"] = (df["resultado_usuario"] == "gano").astype(int)

    # Convertir posiciones numéricas (CSV) a nombres (JSON)
    if pd.api.types.is_numeric_dtype(df["posicion_usuario"]):
        df["posicion_nombre"] = df["posicion_usuario"].apply(
            lambda i: POSICIONES_ORDEN[int(i)] if int(i) < len(POSICIONES_ORDEN) else "N/A"
        )
    else:
        df["posicion_nombre"] = df["posicion_usuario"]

    tabla = (
        df.groupby("posicion_nombre")["victoria"]
        .agg(["mean", "count"])
        .reset_index()
    )

    # Orden lógico
    tabla["orden"] = tabla["posicion_nombre"].apply(lambda x: POSICIONES_ORDEN.index(x) if x in POSICIONES_ORDEN else 99)
    tabla = tabla.sort_values("orden")

    return [
        {
            "posicion": row["posicion_nombre"],
            "winrate": round(row["mean"] * 100, 2),
            "hands": int(row["count"]),
        }
        for _, row in tabla.iterrows()
    ]


# =====================================================
# 3. HISTOGRAMA DE BOTES
# =====================================================
def histograma_botes():
    df = cargar_dataset()
    if df.empty:
        return {"bins": [], "counts": []}

    counts, bins = np.histogram(df["bote_final"], bins=10)
    return {"bins": bins.tolist(), "counts": counts.tolist()}


# =====================================================
# 4. AGRESIVIDAD VS WINRATE
# =====================================================
def agresividad_profit():
    df = cargar_dataset()
    if df.empty:
        return []

    col_aggr = "puntos_estrategia.agresividad" if "puntos_estrategia.agresividad" in df else "agresividad"

    df["victoria"] = (df["resultado_usuario"] == "gano").astype(int)
    df["agresividad_rango"] = pd.cut(
        df[col_aggr],
        bins=5,
        labels=["Muy baja", "Baja", "Media", "Alta", "Muy alta"]
    )

    resultados = []
    for label, serie in df.groupby("agresividad_rango")["victoria"]:
        resultados.append({
            "label": str(label),
            "winrate_promedio": round(serie.mean() * 100, 2)
        })

    return resultados


# =====================================================
# 5. FRECUENCIA POR CATEGORÍA
# =====================================================
def frecuencia_categorias():
    df = cargar_dataset()
    if df.empty:
        return []

    col = "categoria_mano_usuario" if "categoria_mano_usuario" in df else "categoria_mano"
    conteo = Counter(df[col])

    return [{"categoria": c, "cantidad": int(n)} for c, n in conteo.items()]


# =====================================================
# 6. RIESGO VS WINRATE
# =====================================================
def riesgo_winrate():
    df = cargar_dataset()
    if df.empty:
        return []

    col_risk = "puntos_estrategia.riesgo" if "puntos_estrategia.riesgo" in df else "riesgo"

    df["victoria"] = (df["resultado_usuario"] == "gano").astype(int)
    df["riesgo_rango"] = pd.cut(
        df[col_risk],
        bins=5,
        labels=["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto"]
    )

    resultados = []
    for label, serie in df.groupby("riesgo_rango")["victoria"]:
        resultados.append({
            "label": str(label),
            "winrate_promedio": round(serie.mean() * 100, 2)
        })

    return resultados


# =====================================================
# 7. BOTE VS AGRESIVIDAD
# =====================================================
def bote_agresividad():
    df = cargar_dataset()
    if df.empty:
        return []

    col_aggr = "puntos_estrategia.agresividad" if "puntos_estrategia.agresividad" in df else "agresividad"

    df["agresividad_rango"] = pd.cut(
        df[col_aggr],
        bins=5,
        labels=["Muy baja", "Baja", "Media", "Alta", "Muy alta"]
    )

    return [
        {
            "label": str(label),
            "bote_promedio": round(serie.mean(), 2)
        }
        for label, serie in df.groupby("agresividad_rango")["bote_final"]
    ]


# =====================================================
# 8. PROFIT ACUMULADO
# =====================================================
def timeline_profit():
    df = cargar_dataset()
    if df.empty:
        return {"mano_id": [], "profit_acumulado": []}

    if "ganancia_usuario" in df:
        df["profit"] = df["ganancia_usuario"]
    else:
        df["profit"] = df.apply(lambda r: r["bote_final"] if r["resultado_usuario"] == "gano" else -r["bote_final"], axis=1)

    df = df.sort_values("mano_id")
    df["profit_acumulado"] = df["profit"].cumsum()

    return {
        "mano_id": df["mano_id"].tolist(),
        "profit_acumulado": df["profit_acumulado"].tolist(),
    }
