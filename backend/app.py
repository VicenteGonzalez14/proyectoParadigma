from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.generator import generar_dataset
from utils.analyzer import analizar_mano_usuario

from utils.stats import (
    calcular_estadisticas_basicas,
    winrate_por_posicion,
    histograma_botes,
    agresividad_vs_profit,
    frecuencia_categorias,
    riesgo_vs_winrate,
    bote_vs_agresividad,
    timeline_profit
)

app = Flask(__name__)
CORS(app)

# ======================================
# RUTA PRINCIPAL
# ======================================
@app.route("/")
def home():
    return jsonify({"mensaje": "Servidor Flask funcionando correctamente."})


# ======================================
# GENERAR DATASET
# ======================================
@app.route("/api/generar", methods=["POST"])
def generar():
    data = request.get_json() or {}
    num = data.get("num_manos", 5000)
    print(f"📦 Solicitud para generar dataset con {num} manos...")
    resultado = generar_dataset(num)
    print("✅ Dataset generado")
    return jsonify(resultado)


# ======================================
# ESTADÍSTICAS BÁSICAS
# ======================================
@app.route("/api/estadisticas", methods=["GET"])
def estadisticas():
    return jsonify(calcular_estadisticas_basicas())


# ======================================
# ANALIZAR MANO
# ======================================
@app.route("/api/analizar", methods=["POST"])
def analizar_mano():
    datos_mano = request.get_json()
    if not datos_mano:
        return jsonify({"error": "No se recibieron datos"}), 400

    resultado = analizar_mano_usuario(datos_mano)

    if "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado)


# ======================================
# ENDPOINTS GRÁFICOS (EP3 / EF3)
# ======================================
@app.route("/api/charts/winrate-posicion", methods=["GET"])
def chart_winrate_posicion():
    return jsonify(winrate_por_posicion())


@app.route("/api/charts/histograma-botes", methods=["GET"])
def chart_histograma_botes():
    bins = request.args.get("bins", default=10, type=int)
    return jsonify(histograma_botes(bins))


@app.route("/api/charts/agresividad-profit", methods=["GET"])
def chart_agresividad_profit():
    return jsonify(agresividad_vs_profit())


@app.route("/api/charts/frecuencia-categorias", methods=["GET"])
def chart_frecuencia():
    return jsonify(frecuencia_categorias())


@app.route("/api/charts/riesgo-winrate", methods=["GET"])
def chart_riesgo():
    return jsonify(riesgo_vs_winrate())


@app.route("/api/charts/bote-agresividad", methods=["GET"])
def chart_bote_agres():
    return jsonify(bote_vs_agresividad())


@app.route("/api/charts/timeline-profit", methods=["GET"])
def chart_timeline():
    return jsonify(timeline_profit())


if __name__ == "__main__":
    app.run(debug=True)