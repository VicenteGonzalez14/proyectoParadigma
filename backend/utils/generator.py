import json
import random
import math
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "poker_dataset.json"

VALORES = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
PALOS = ["♠","♥","♦","♣"]
MAZO = [v+p for v in VALORES for p in PALOS]

def evaluar_mano(cartas_usuario, cartas_comunitarias):
    valores = [c[:-1] for c in cartas_usuario + cartas_comunitarias]
    palos = [c[-1] for c in cartas_usuario + cartas_comunitarias]

    valor_map = {
        "A": 14, "K": 13, "Q": 12, "J": 11,
        "10": 10, "9": 9, "8": 8, "7": 7,
        "6": 6, "5": 5, "4": 4, "3": 3, "2": 2
    }

    nums = sorted([valor_map[v] for v in valores], reverse=True)
    par = len(nums) != len(set(nums))
    doble_par = len(nums) - len(set(nums)) >= 2
    trio = any(nums.count(n) == 3 for n in nums)
    color = any(palos.count(p) >= 5 for p in palos)

    unique_nums = sorted(list(set(nums)))
    if 14 in unique_nums:
        unique_nums.insert(0,1)

    escalera = False
    for i in range(len(unique_nums)-4):
        if all(unique_nums[i+k]==unique_nums[i]+k for k in range(5)):
            escalera=True

    if color and escalera: return "Escalera de Color"
    if any(nums.count(n)==4 for n in nums): return "Póker"
    if trio and par: return "Full"
    if color: return "Color"
    if escalera: return "Escalera"
    if trio: return "Trío"
    if doble_par: return "Doble Par"
    if par: return "Par"
    return "Carta Alta"


def generar_dataset(num_manos=5000, usuario_id="Jugador_1"):
    posiciones_reales = ["SB","BB","UTG","UTG+1","MP","LJ","HJ","CO","BTN"]
    jugadores_posibles = [f"Jugador_{i}" for i in range(1,10)]
    dataset = []

    for mano_id in range(1, num_manos+1):
        num_jug = random.randint(2,9)
        jugadores = random.sample(jugadores_posibles, num_jug)

        if usuario_id not in jugadores:
            jugadores[random.randint(0,num_jug-1)] = usuario_id

        posiciones = posiciones_reales[:num_jug]
        random.shuffle(jugadores)
        pos_map = {jug:pos for jug,pos in zip(jugadores,posiciones)}
        pos_usuario = pos_map[usuario_id]

        mazo = MAZO.copy()
        random.shuffle(mazo)

        cartas_usuario = mazo[:2]
        cartas_com = mazo[2:7]

        rondas = [
            {"nombre": "Preflop", "acciones": random.choices(["check","call","raise","fold"], k=2)},
            {"nombre": "Flop",    "acciones": random.choices(["check","call","raise","fold"], k=2)},
            {"nombre": "Turn",    "acciones": random.choices(["check","call","raise","fold"], k=2)},
            {"nombre": "River",   "acciones": random.choices(["check","call","raise","fold"], k=2)},
        ]

        bote = random.randint(80,900)

        agres = round(random.uniform(0,1),2)
        riesgo = round(random.uniform(0,1),2)

        categoria = evaluar_mano(cartas_usuario, cartas_com)

        gano = random.random() < 0.45

        dataset.append({
            "mano_id": mano_id,
            "usuario_id": usuario_id,
            "jugadores_mesa": jugadores,
            "posicion_usuario": pos_usuario,
            "cartas_usuario": cartas_usuario,
            "cartas_comunitarias": cartas_com,
            "categoria_mano_usuario": categoria,
            "resultado_usuario": "gano" if gano else "perdio",
            "bote_final": bote,
            "ganancia_usuario": bote if gano else -bote,
            "puntos_estrategia": {
                "agresividad": agres,
                "riesgo": riesgo
            },
            "rondas": rondas
        })

    DATA_PATH.parent.mkdir(exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset,f,indent=4,ensure_ascii=False)

    return {"status":"ok","mensaje":"Dataset generado correctamente"}
