# En: backend/utils/analyzer.py

# ¡Reutilizamos las funciones que ya creaste en generator.py!
from .generator import (
    evaluar_mano, 
    probabilidad_victoria_mejorada, 
    contar_acciones_agresivas
)

def analizar_mano_usuario(datos_mano):
    """
    Analiza una mano específica proporcionada por el usuario.
    'datos_mano' es un diccionario que viene del frontend.
    Ej: { "cartas_usuario": ["A♠", "K♥"], "cartas_comunitarias": ["Q♦", "J♣", "10♠"] }
    """
    try:
        cartas_usuario = datos_mano.get("cartas_usuario", [])
        cartas_comunitarias = datos_mano.get("cartas_comunitarias", [])

        if len(cartas_usuario) < 2:
            return {"error": "Se requieren 2 cartas de usuario."}

        # 1. Evaluar la categoría de la mano (usando tu función existente)
        categoria = evaluar_mano(cartas_usuario, cartas_comunitarias)

        # 2. Simular probabilidad de victoria (simplificado)
        # Como no tenemos acciones del usuario, usamos valores neutros
        rondas_simuladas = [{"nombre": "Preflop", "acciones": ["check", "call"]}]
        estrategia_simulada = {"agresividad": 0.5, "riesgo": 0.5}
        n_rivales = datos_mano.get("n_rivales", 3) # Asumimos 3 rivales

        prob_ganar = probabilidad_victoria_mejorada(
            categoria,
            rondas_simuladas,
            n_rivales,
            estrategia_simulada
        )

        prob_perder = 1.0 - prob_ganar

        # 3. Devolver el resultado
        return {
            "categoria_mano": categoria,
            "probabilidad_victoria": round(prob_ganar * 100, 2),
            "probabilidad_derrota": round(prob_perder * 100, 2),
            "cartas_analizadas": cartas_usuario + cartas_comunitarias
        }

    except Exception as e:
        # Captura cualquier error (ej. una carta mal escrita)
        return {"error": f"Error al analizar la mano: {str(e)}"}