from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.generator import generar_dataset
from utils.stats import calcular_estadisticas_basicas
from utils.analyzer import analizar_mano_usuario

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"mensaje": "Servidor Flask funcionando correctamente."})

@app.route("/api/generar", methods=["POST"])
def generar():
    data = request.get_json() or {}
    num = data.get("num_manos", 5000)
    print(f"📦 Recibida solicitud para generar dataset con {num} manos")
    resultado = generar_dataset(num)
    print("✅ Dataset generado")
    return jsonify(resultado)

@app.route("/api/estadisticas", methods=["GET"])
def estadisticas():
    resultado = calcular_estadisticas_basicas()
    return jsonify(resultado)

@app.route("/api/analizar", methods=["POST"])
def analizar_mano():
    """
    Recibe datos de una mano del usuario (JSON) y devuelve su análisis.
    """
    datos_mano = request.get_json()
    if not datos_mano:
        return jsonify({"error": "No se recibieron datos"}), 400

    print(f"📦 Recibida solicitud para analizar: {datos_mano}")

    # Llama a tu nueva lógica de análisis
    resultado = analizar_mano_usuario(datos_mano)

    if "error" in resultado:
        # Si el analizador devolvió un error (ej. "Se requieren 2 cartas")
        return jsonify(resultado), 400

    print(f"📈 Resultado del análisis: {resultado}")
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)