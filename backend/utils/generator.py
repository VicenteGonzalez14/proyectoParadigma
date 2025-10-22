import json
import random
import math
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "poker_dataset.json"

# -------------------------
# Funciones auxiliares
# -------------------------

def evaluar_mano(cartas_usuario, cartas_comunitarias):
    """Evalúa la mano del jugador (simplificada, sin librerías externas)."""
    cartas = cartas_usuario + cartas_comunitarias
    valores = [c[:-1] for c in cartas]
    palos = [c[-1] for c in cartas]

    valor_map = {
        "A": 14, "K": 13, "Q": 12, "J": 11,
        "10": 10, "9": 9, "8": 8, "7": 7, "6": 6,
        "5": 5, "4": 4, "3": 3, "2": 2
    }
    nums = sorted([valor_map[v] for v in valores], reverse=True)

    par = len(valores) != len(set(valores))
    doble_par = len(valores) - len(set(valores)) >= 2
    trio = any(valores.count(v) == 3 for v in valores)
    color = any(palos.count(p) >= 5 for p in palos)
    escalera = any(all(n - i in nums for i in range(5)) for n in range(14, 5, -1))

    if color and escalera:
        return "Escalera de Color"
    elif trio and par:
        return "Full"
    elif trio:
        return "Trío"
    elif doble_par:
        return "Doble Par"
    elif par:
        return "Par"
    elif escalera:
        return "Escalera"
    elif color:
        return "Color"
    else:
        return "Carta Alta"

def sigmoid(x):
    """Función sigmoide para escalar valores entre 0 y 1."""
    return 1 / (1 + math.exp(-x))

BASE_HAND_WIN = {
    "Escalera de Color": 0.95,
    "Póker": 0.90,
    "Full": 0.85,
    "Color": 0.75,
    "Escalera": 0.70,
    "Trío": 0.60,
    "Doble Par": 0.50,
    "Par": 0.40,
    "Carta Alta": 0.22
}

AGGRESSIVE_SET = {"raise", "all-in"}

def contar_acciones_agresivas(rondas):
    """Cuenta acciones agresivas (raise/all-in) en todas las rondas."""
    total = 0
    por_ronda = []
    for r in rondas:
        aggr = sum(1 for a in r.get("acciones", []) if a in AGGRESSIVE_SET)
        total += aggr
        por_ronda.append(aggr)
    return {"total": total, "por_ronda": por_ronda}

def fold_equity(agresividad, riesgo, acciones_agresivas, n_rivales, ronda_idx):
    """
    Modelo simple de fold equity (probabilidad de que los rivales se retiren).
    Aumenta con agresividad, riesgo y número de acciones agresivas.
    Disminuye con más rivales y en calles tardías.
    """
    w0 = -0.8
    w_aggr = 1.4
    w_risk = 0.8
    w_act = 0.5
    w_rivals = -0.55
    w_street = -0.35

    x = (
        w0
        + w_aggr * agresividad
        + w_risk * riesgo
        + w_act * acciones_agresivas
        + w_rivals * max(n_rivales, 1)
        + w_street * ronda_idx
    )
    return sigmoid(x)

def probabilidad_victoria_mejorada(categoria, rondas, n_rivales, puntos_estrategia):
    """Combina fuerza real de la mano + fold equity (bluffeo)."""
    p_mano = BASE_HAND_WIN.get(categoria, 0.3)
    agresividad = float(puntos_estrategia.get("agresividad", 0.5))
    riesgo = float(puntos_estrategia.get("riesgo", 0.5))

    acc = contar_acciones_agresivas(rondas)
    acciones_total = acc["total"]
    ronda_idx = max((i for i, r in enumerate(rondas) if r.get("acciones")), default=0)

    p_fold = fold_equity(agresividad, riesgo, acciones_total, n_rivales, ronda_idx)

    p_total = p_mano + (1 - p_mano) * p_fold  # prob ganar o hacer foldear
    return max(0.03, min(0.98, p_total))

# -------------------------
# Generador principal
# -------------------------

def generar_dataset(num_manos=5000, usuario_id="Jugador_1"):
    """Genera dataset realista de Texas Hold'em centrado en un solo jugador."""
    rondas_nombres = ["Preflop", "Flop", "Turn", "River", "Showdown"]

    valores = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
    palos = ["♠","♥","♦","♣"]
    cartas_totales = [f"{v}{p}" for v in valores for p in palos]
    jugadores_base = [f"Jugador_{i}" for i in range(1, 10)]

    dataset = []

    for mano_id in range(1, num_manos + 1):
        mesa = random.randint(1, 5)
        num_jugadores = random.randint(2, 9)
        jugadores = random.sample(jugadores_base, num_jugadores)
        if usuario_id not in jugadores:
            jugadores[random.randint(0, num_jugadores - 1)] = usuario_id

        # Cartas únicas
        cartas_disponibles = cartas_totales.copy()
        cartas_usuario = random.sample(cartas_disponibles, 2)
        for c in cartas_usuario:
            cartas_disponibles.remove(c)

        flop = random.sample(cartas_disponibles, 3)
        for c in flop: cartas_disponibles.remove(c)
        turn = random.sample(cartas_disponibles, 1)
        for c in turn: cartas_disponibles.remove(c)
        river = random.sample(cartas_disponibles, 1)
        cartas_comunitarias = flop + turn + river

        # Puntos de estilo de juego
        puntos_estrategia = {
            "agresividad": round(random.uniform(0, 1), 2),
            "paciencia": round(random.uniform(0, 1), 2),
            "riesgo": round(random.uniform(0, 1), 2)
        }

        # Rondas y bote
        rondas = []
        bote = 0
        for nombre in rondas_nombres:
            acciones = random.choices(
                ["check", "call", "raise", "fold", "all-in"],
                k=random.randint(1, 3)
            )
            bote += random.randint(50, 500)
            rondas.append({
                "nombre": nombre,
                "acciones": acciones,
                "bote_parcial": bote
            })

        # Evaluación de mano y bluffeo
        categoria = evaluar_mano(cartas_usuario, cartas_comunitarias)
        n_rivales = max(len(jugadores) - 1, 1)
        prob_ganar = probabilidad_victoria_mejorada(categoria, rondas, n_rivales, puntos_estrategia)
        gano = random.random() < prob_ganar

        resultado_usuario = "gano" if gano else "perdio"
        ganador = usuario_id if gano else random.choice([j for j in jugadores if j != usuario_id])

        mano = {
            "mano_id": mano_id,
            "mesa": mesa,
            "usuario_id": usuario_id,
            "jugadores_mesa": jugadores,
            "cartas_usuario": cartas_usuario,
            "cartas_comunitarias": cartas_comunitarias,
            "categoria_mano_usuario": categoria,
            "rondas": rondas,
            "resultado_usuario": resultado_usuario,
            "bote_final": bote,
            "ganador": ganador,
            "puntos_estrategia": puntos_estrategia,
            "probabilidad_victoria": round(prob_ganar, 3)
        }

        dataset.append(mano)

    # Guardar dataset
    DATA_PATH.parent.mkdir(exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print(f"✅ Dataset generado con {num_manos} manos del jugador {usuario_id}.")
    return {"status": "ok", "mensaje": f"Dataset generado con {num_manos} manos del jugador {usuario_id}."}