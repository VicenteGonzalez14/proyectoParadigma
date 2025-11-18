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

# =============================================
# 1. WINRATE POR POSICIÓN
# =============================================
def winrate_por_posicion():
    """
    Calcula el winrate agrupado por posición.
    Como el dataset no tiene una columna "posicion", generamos una derivada:
        posición = número de jugadores en la mesa
    """
    df = cargar_dataset()

    # Crear posición derivada
    df["posicion"] = df["jugadores_mesa"].apply(lambda x: len(x))
    df["victoria"] = (df["resultado_usuario"] == "gano").astype(int)

    tabla = (
        df.groupby("posicion")["victoria"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "winrate", "count": "hands"})
    )

    tabla["winrate"] = (tabla["winrate"] * 100).round(2)

    return tabla.to_dict(orient="records")


# =============================================
# 2. HISTOGRAMA DE BOTES
# =============================================
def histograma_botes(bins=10):
    """
    Devuelve un histograma del tamaño de bote final.
    """
    df = cargar_dataset()

    cortes = pd.cut(df["bote_final"], bins=bins)
    counts = cortes.value_counts(sort=False)

    return {
        "bins": counts.index.astype(str).tolist(),
        "counts": counts.values.tolist()
    }


# =============================================
# 3. AGRESIVIDAD VS PROFIT
# =============================================
def agresividad_vs_profit():
    """
    Relación entre agresividad y probabilidad de ganar.
    Usa buckets de agresividad y calcula winrate promedio por bucket.
    """

    df = cargar_dataset()

    df["agresividad"] = df["puntos_estrategia.agresividad"]
    df["victoria"] = (df["resultado_usuario"] == "gano").astype(int)

    buckets = pd.qcut(df["agresividad"], q=5, duplicates="drop")

    tabla = (
        df.groupby(buckets)
        .agg(
            agresividad_promedio=("agresividad", "mean"),
            winrate_promedio=("victoria", "mean")
        )
        .reset_index()
    )

    tabla["winrate_promedio"] = (tabla["winrate_promedio"] * 100).round(2)
    tabla["agresividad_promedio"] = tabla["agresividad_promedio"].round(2)

    tabla["label"] = tabla["agresividad"].astype(str)

    return tabla[["label", "agresividad_promedio", "winrate_promedio"]].to_dict(orient="records")


# =============================================
# 4. FRECUENCIA DE CATEGORÍAS DE MANO
# =============================================
def frecuencia_categorias():
    """
    Cuenta cuántas veces aparece cada categoría de mano.
    Perfecto para gráficos de barra o torta.
    """
    df = cargar_dataset()

    tabla = (
        df["categoria_mano_usuario"]
        .value_counts()
        .rename_axis("categoria")
        .reset_index(name="cantidad")
    )

    return tabla.to_dict(orient="records")

# =============================================
# 5. RIESGO VS WINRATE
# =============================================
def riesgo_vs_winrate():
    df = cargar_dataset()

    df["riesgo"] = df["puntos_estrategia.riesgo"]
    df["victoria"] = (df["resultado_usuario"] == "gano").astype(int)

    grouped = (
        df.groupby(pd.qcut(df["riesgo"], q=5, duplicates="drop"))
        .agg(
            riesgo_promedio=("riesgo", "mean"),
            winrate_promedio=("victoria", "mean")
        )
        .reset_index()
    )

    grouped["riesgo_promedio"] = grouped["riesgo_promedio"].round(2)
    grouped["winrate_promedio"] = (grouped["winrate_promedio"] * 100).round(2)

    grouped["label"] = grouped["riesgo"].astype(str)

    return grouped[["label", "riesgo_promedio", "winrate_promedio"]].to_dict(orient="records")


# =============================================
# 6. BOTE FINAL VS AGRESIVIDAD
# =============================================
def bote_vs_agresividad():
    df = cargar_dataset()

    df["agresividad"] = df["puntos_estrategia.agresividad"]

    grouped = (
        df.groupby(pd.qcut(df["agresividad"], q=5, duplicates="drop"))
        .agg(
            agresividad_promedio=("agresividad", "mean"),
            bote_promedio=("bote_final", "mean")
        )
        .reset_index()
    )

    grouped["agresividad_promedio"] = grouped["agresividad_promedio"].round(2)
    grouped["bote_promedio"] = grouped["bote_promedio"].round(2)

    grouped["label"] = grouped["agresividad"].astype(str)

    return grouped[["label", "agresividad_promedio", "bote_promedio"]].to_dict(orient="records")


# =============================================
# 7. PROFIT TIMELINE (GANANCIA ACUMULADA)
# =============================================
def timeline_profit():
    df = cargar_dataset()

    # Convertimos "gano"/"perdio" a profit real (1 o -1)
    df["profit"] = df["resultado_usuario"].apply(lambda x: 1 if x == "gano" else -1)

    df = df.sort_values("mano_id")
    df["profit_acumulado"] = df["profit"].cumsum()

    return {
        "mano_id": df["mano_id"].tolist(),
        "profit_acumulado": df["profit_acumulado"].tolist()
    }