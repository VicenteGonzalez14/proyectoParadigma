from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.generator import generar_dataset
from utils.stats import calcular_estadisticas_basicas

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

if __name__ == "__main__":
    app.run(debug=True)