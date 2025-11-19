import random
import math
from collections import Counter
from pathlib import Path
import json

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "poker_dataset.json"

VALORES = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
PALOS = ["♠","♥","♦","♣"]
MAZO = [v+p for v in VALORES for p in PALOS]

VALOR_MAP = {
    "A":14, "K":13, "Q":12, "J":11,
    "10":10,"9":9,"8":8,"7":7,"6":6,
    "5":5,"4":4,"3":3,"2":2
}

POSICIONES = ["SB","BB","UTG","UTG+1","MP","LJ","HJ","CO","BTN"]


# ======================================================
# CARGAR DATASET
# ======================================================
def cargar_dataset():
    if not DATA_PATH.exists():
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# ======================================================
# EVALUADOR DE MANO
# ======================================================
def evaluar_mano_total(cartas):
    valores = [c[:-1] for c in cartas]
    palos = [c[-1] for c in cartas]

    nums = sorted([VALOR_MAP[v] for v in valores], reverse=True)
    counts = Counter(nums)

    # COLOR
    es_color = any(palos.count(p) >= 5 for p in PALOS)

    # ESCALERA
    unicos = sorted(list(set(nums)))
    if 14 in unicos:
        unicos.insert(0, 1)

    es_escalera = False
    for i in range(len(unicos)-4):
        if all(unicos[i+k] == unicos[i] + k for k in range(5)):
            es_escalera = True

    if es_color and es_escalera: return ("Escalera de Color", 9)
    if 4 in counts.values(): return ("Póker", 8)
    if 3 in counts.values() and 2 in counts.values(): return ("Full", 7)
    if es_color: return ("Color", 6)
    if es_escalera: return ("Escalera", 5)
    if 3 in counts.values(): return ("Trío", 4)
    if list(counts.values()).count(2) >= 2: return ("Doble Par", 3)
    if 2 in counts.values(): return ("Par", 2)

    return ("Carta Alta", 1)


# ======================================================
# EQUITY (SIMULACIÓN MONTECARLO)
# ======================================================
def equity(cartas_user, cartas_mesa, n=500):
    usadas = set(cartas_user + cartas_mesa)
    mazo_rest = [c for c in MAZO if c not in usadas]

    wins = ties = 0
    faltan = 5 - len(cartas_mesa)

    for _ in range(n):
        tmp = mazo_rest.copy()
        random.shuffle(tmp)

        rival = tmp[:2]
        mesa = cartas_mesa + tmp[2:2+faltan]

        _, ru = evaluar_mano_total(cartas_user + mesa)
        _, rr = evaluar_mano_total(rival + mesa)

        if ru > rr: wins += 1
        elif ru == rr: ties += 1

    return (wins + ties*0.5) / n


# ======================================================
# OUTS
# ======================================================
def outs(cartas_user, mesa):
    if len(mesa) < 3 or len(mesa) >= 5:
        return 0, []

    usadas = set(cartas_user + mesa)
    mazo_rest = [c for c in MAZO if c not in usadas]
    base_rank = evaluar_mano_total(cartas_user + mesa)[1]

    outs_list = []
    for c in mazo_rest:
        r = evaluar_mano_total(cartas_user + mesa + [c])[1]
        if r > base_rank:
            outs_list.append(c)

    return len(outs_list), outs_list


# ======================================================
# RECOMENDACIÓN SEGÚN EQUITY
# ======================================================
def recomendacion_equity(e):
    if e > 0.70:
        return "Tienes una ventaja clara. Buen momento para apostar agresivo."
    if e > 0.55:
        return "Tu equity es sólida. Puedes presionar a tus rivales."
    if e > 0.40:
        return "Equity media. Juega con precaución."
    if e > 0.25:
        return "Estás por detrás. Evita botes grandes."
    return "Muy mala equity. Solo continúa si tienes odds claras."


# ======================================================
# ANALIZADOR PRINCIPAL FASE POR FASE
# ======================================================
def analizar_mano_fases(req):
    cartas_user = req["cartas_usuario"]
    posicion = req.get("posicion", "MP")

    # GENERAR FLOP, TURN, RIVER
    usadas = set(cartas_user)
    mazo_rest = [c for c in MAZO if c not in usadas]
    random.shuffle(mazo_rest)

    flop = mazo_rest[:3]
    turn = mazo_rest[3]
    river = mazo_rest[4]

    # ==========================
    # PRE-FLOP
    # ==========================
    cat_pre, _ = evaluar_mano_total(cartas_user)
    eq_pre = round(equity(cartas_user, []), 2)
    rec_pre = recomendacion_equity(eq_pre)

    # ==========================
    # FLOP
    # ==========================
    cat_flop, _ = evaluar_mano_total(cartas_user + flop)
    eq_flop = round(equity(cartas_user, flop), 2)
    o_flop, olist_flop = outs(cartas_user, flop)
    rec_flop = recomendacion_equity(eq_flop)

    # ==========================
    # TURN
    # ==========================
    mesa_turn = flop + [turn]
    cat_turn, _ = evaluar_mano_total(cartas_user + mesa_turn)
    eq_turn = round(equity(cartas_user, mesa_turn), 2)
    o_turn, olist_turn = outs(cartas_user, mesa_turn)
    rec_turn = recomendacion_equity(eq_turn)

    # ==========================
    # RIVER
    # ==========================
    mesa_river = mesa_turn + [river]
    cat_river, _ = evaluar_mano_total(cartas_user + mesa_river)
    eq_river = round(equity(cartas_user, mesa_river), 2)
    rec_river = recomendacion_equity(eq_river)

    # =======================================================
    # ANÁLISIS GENERAL (NUEVO)
    # =======================================================
    promedio_equity = (eq_pre + eq_flop + eq_turn + eq_river) / 4

    if promedio_equity > 0.70:
        analisis_general = (
            "Tu equity global es muy fuerte. La mano dominó la mayoría de las fases "
            "y es competitiva incluso contra rangos amplios."
        )
    elif promedio_equity > 0.55:
        analisis_general = (
            "Tu mano muestra solidez general. Puedes jugar agresivo en muchas situaciones."
        )
    elif promedio_equity > 0.40:
        analisis_general = (
            "Tu mano tiene fuerza media. Se recomienda cautela según tamaño del bote y rivales."
        )
    else:
        analisis_general = (
            "Tu mano estuvo por detrás en varias fases. Debes evitar involucrarte en botes grandes."
        )

    # =======================================================
    # RECOMENDACIÓN FINAL (NUEVO)
    # =======================================================
    if eq_river > 0.70:
        recomendacion_final = "Mano fuerte. Puedes apostar por valor o incluso ir all-in."
    elif eq_river > 0.55:
        recomendacion_final = "Buena equity final. Apuesta por valor contra rangos amplios."
    elif eq_river > 0.40:
        recomendacion_final = "Equity decente pero no excelente. Controla el tamaño del bote."
    elif eq_river > 0.25:
        recomendacion_final = "Débil en el river. Solo paga apuestas pequeñas."
    else:
        recomendacion_final = "Fold en la mayoría de escenarios."

    return {
        "preflop": {
            "categoria": cat_pre,
            "equity": eq_pre,
            "recomendacion": rec_pre
        },
        "flop": {
            "cartas": flop,
            "categoria": cat_flop,
            "equity": eq_flop,
            "outs": o_flop,
            "outs_list": olist_flop,
            "recomendacion": rec_flop
        },
        "turn": {
            "carta": turn,
            "categoria": cat_turn,
            "equity": eq_turn,
            "outs": o_turn,
            "outs_list": olist_turn,
            "recomendacion": rec_turn
        },
        "river": {
            "carta": river,
            "categoria": cat_river,
            "equity": eq_river,
            "recomendacion": rec_river
        },
        "equity_evolucion": [eq_pre, eq_flop, eq_turn, eq_river],
        "cartas_finales": cartas_user + flop + [turn, river],
        "posicion": posicion,

        # LOS CAMPOS QUE TU FRONTEND NECESITA
        "analisis_general": analisis_general,
        "recomendacion_final": recomendacion_final
    }