from flask import Flask, jsonify, request
from flask_cors import CORS

# ==========================
# IMPORTAR UTILIDADES
# ==========================
from utils.generator import generar_dataset
from utils.analyzer import analizar_mano_fases
from utils.stats import (
    estadisticas_generales,
    winrate_por_posicion,
    histograma_botes,
    agresividad_profit,
    frecuencia_categorias,
    riesgo_winrate,
    bote_agresividad,
    timeline_profit,
)

# ==========================
# CONFIGURACIÓN FLASK
# ==========================
app = Flask(__name__)

# CORS completamente abierto
CORS(app, resources={r"/*": {"origins": "*"}})


# ==========================
# HOME
# ==========================
@app.route("/")
def home():
    return jsonify({"mensaje": "Servidor Flask funcionando correctamente."})


# ==========================
# DATASET
# ==========================
@app.route("/api/generar", methods=["POST"])
def generar():
    data = request.get_json() or {}
    num_manos = data.get("num_manos", 5000)

    generar_dataset(num_manos=num_manos)

    response = jsonify({"mensaje": "Dataset generado", "num_manos": num_manos})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# ==========================
# ESTADÍSTICAS
# ==========================
@app.route("/api/estadisticas", methods=["GET"])
def stats():
    data = estadisticas_generales()

    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# ==========================
# ANALIZADOR — *PREVIO* (tu versión antigua)
# ==========================
@app.route("/api/analizar", methods=["POST"])
def analizar():
    req = request.get_json()
    result = analizar_mano_fases(req)

    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# ==========================
# ANALIZAR FASE POR FASE — NUEVO
# ==========================
@app.route("/api/analizar-fases", methods=["POST", "OPTIONS"])
def analizar_fases():
    # --- Responder preflight CORS ---
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    # --- Procesar POST normal ---
    req = request.get_json()
    result = analizar_mano_fases(req)

    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# ==========================
# GRÁFICOS
# ==========================
@app.route("/api/charts/winrate-posicion", methods=["GET"])
def api_winrate_posicion():
    response = jsonify(winrate_por_posicion())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/charts/histograma-botes", methods=["GET"])
def api_histograma_botes():
    response = jsonify(histograma_botes())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/charts/agresividad-profit", methods=["GET"])
def api_agresividad_profit():
    response = jsonify(agresividad_profit())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/charts/frecuencia-categorias", methods=["GET"])
def api_frecuencia_categorias():
    response = jsonify(frecuencia_categorias())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/charts/riesgo-winrate", methods=["GET"])
def api_riesgo_winrate():
    response = jsonify(riesgo_winrate())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/charts/bote-agresividad", methods=["GET"])
def api_bote_agresividad():
    response = jsonify(bote_agresividad())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/charts/timeline-profit", methods=["GET"])
def api_timeline_profit():
    response = jsonify(timeline_profit())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
