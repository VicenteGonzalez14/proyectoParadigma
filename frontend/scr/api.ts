const BASE_URL = "http://127.0.0.1:5000/api";

async function fetchJSON(url: string, options: any = {}) {
    const res = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options
    });

    if (!res.ok) throw new Error(`Error en la solicitud: ${url}`);
    return res.json();
}

/* ============================================================
   ESTADÍSTICAS GENERALES
============================================================ */
export async function obtenerEstadisticas() {
    return fetchJSON(`${BASE_URL}/estadisticas`);
}

export async function generarDataset() {
    return fetchJSON(`${BASE_URL}/generar`, {
        method: "POST",
        body: JSON.stringify({})
    });
}

/* ============================================================
   ANALIZADOR POR FASES
============================================================ */
export async function analizarMano(payload: {
    cartas_usuario: string[];
    cartas_comunitarias?: string[];   // ahora OPCIONAL pero permitido
    posicion: string;
}) {
    // aseguramos que nunca vaya undefined
    const fixedPayload = {
        cartas_usuario: payload.cartas_usuario,
        cartas_comunitarias: payload.cartas_comunitarias ?? [],
        posicion: payload.posicion
    };

    return fetchJSON(`${BASE_URL}/analizar`, {
        method: "POST",
        body: JSON.stringify(fixedPayload)
    });
}

/* ============================================================
   GRÁFICOS – FORMATO COMPATIBLE CON CHART.JS
============================================================ */

export async function obtenerWinratePosicion() {
    const data = await fetchJSON(`${BASE_URL}/charts/winrate-posicion`);

    return {
        tipo: "bar",
        chart: {
            data: {
                labels: data.map((x: any) => x.posicion),
                datasets: [{
                    label: "Winrate %",
                    data: data.map((x: any) => x.winrate),
                    backgroundColor: "#3498db"
                }]
            },
            options: { responsive: true }
        }
    };
}

export async function obtenerHistogramaBotes() {
    const data = await fetchJSON(`${BASE_URL}/charts/histograma-botes`);

    return {
        tipo: "bar",
        chart: {
            data: {
                labels: data.bins.map((b: number) => b.toFixed(0)),
                datasets: [{
                    label: "Frecuencia",
                    data: data.counts,
                    backgroundColor: "#9b59b6"
                }]
            },
            options: { responsive: true }
        }
    };
}

export async function obtenerAgresividadProfit() {
    const data = await fetchJSON(`${BASE_URL}/charts/agresividad-profit`);

    return {
        tipo: "bar",
        chart: {
            data: {
                labels: data.map((x: any) => x.label),
                datasets: [{
                    label: "Winrate %",
                    data: data.map((x: any) => x.winrate_promedio),
                    backgroundColor: "#1abc9c"
                }]
            },
            options: { responsive: true }
        }
    };
}

export async function obtenerFrecuenciaCategorias() {
    const data = await fetchJSON(`${BASE_URL}/charts/frecuencia-categorias`);

    return {
        tipo: "bar",
        chart: {
            data: {
                labels: data.map((x: any) => x.categoria),
                datasets: [{
                    label: "Cantidad",
                    data: data.map((x: any) => x.cantidad),
                    backgroundColor: "#f1c40f"
                }]
            },
            options: { responsive: true }
        }
    };
}

export async function obtenerRiesgoWinrate() {
    const data = await fetchJSON(`${BASE_URL}/charts/riesgo-winrate`);

    return {
        tipo: "line",
        chart: {
            data: {
                labels: data.map((x: any) => x.label),
                datasets: [{
                    label: "Winrate %",
                    data: data.map((x: any) => x.winrate_promedio),
                    borderColor: "#e74c3c"
                }]
            },
            options: { responsive: true }
        }
    };
}

export async function obtenerBoteAgresividad() {
    const data = await fetchJSON(`${BASE_URL}/charts/bote-agresividad`);

    return {
        tipo: "line",
        chart: {
            data: {
                labels: data.map((x: any) => x.label),
                datasets: [{
                    label: "Bote promedio",
                    data: data.map((x: any) => x.bote_promedio),
                    borderColor: "#8e44ad"
                }]
            },
            options: { responsive: true }
        }
    };
}

export async function obtenerTimelineProfit() {
    const data = await fetchJSON(`${BASE_URL}/charts/timeline-profit`);

    return {
        tipo: "line",
        chart: {
            data: {
                labels: data.mano_id,
                datasets: [{
                    label: "Profit acumulado",
                    data: data.profit_acumulado,
                    borderColor: "#2ecc71"
                }]
            },
            options: { responsive: true }
        }
    };
}
