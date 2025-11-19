declare const Chart: any;

import {
    obtenerEstadisticas,
    generarDataset,
    analizarMano,
    obtenerWinratePosicion,
    obtenerHistogramaBotes,
    obtenerAgresividadProfit,
    obtenerFrecuenciaCategorias,
    obtenerRiesgoWinrate,
    obtenerBoteAgresividad,
    obtenerTimelineProfit
} from "./api.js";

let statsDiv: HTMLElement;
let errorPanel: HTMLElement;

let equityChart: any = null;
let dynamicChart: any = null;

/* ==================================================
   ESTADÍSTICAS GENERALES
================================================== */
function mostrarEstadisticas(data: any) {
    statsDiv.innerHTML = `
        <ul>
            <li><strong>Total de manos:</strong> ${data.total_manos}</li>
            <li><strong>Ganadas:</strong> ${data.ganadas}</li>
            <li><strong>Perdidas:</strong> ${data.perdidas}</li>
            <li><strong>Tasa de victoria:</strong> ${data.tasa_victoria}%</li>
            <li><strong>Bote promedio:</strong> ${data.bote_promedio}</li>
            <li><strong>Total ganado:</strong> ${data.total_ganado}</li>
            <li><strong>Total perdido:</strong> ${data.total_perdido}</li>
            <li><strong>Profit neto:</strong> ${data.profit_neto}</li>
            <li><strong>Agresividad media:</strong> ${data.agresividad_media}</li>
            <li><strong>Riesgo medio:</strong> ${data.riesgo_medio}</li>
        </ul>`;
}

async function cargarEstadisticas() {
    try {
        const data = await obtenerEstadisticas();
        mostrarEstadisticas(data);
    } catch {
        errorPanel.classList.remove("hidden");
    }
}

/* ==================================================
   GRÁFICO EVOLUCIÓN DE EQUITY
================================================== */
function dibujarGraficoEvolucion(eqs: number[]) {
    const ctx = document.getElementById("equity-phase-chart") as HTMLCanvasElement;

    if (equityChart) equityChart.destroy();

    equityChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Preflop", "Flop", "Turn", "River"],
            datasets: [
                {
                    label: "Equity %",
                    data: eqs.map(x => Math.round(x * 100)),
                    borderColor: "#1abc9c",
                    tension: 0.2
                }
            ]
        },
        options: { responsive: true }
    });
}

/* ==================================================
   MOSTRAR RESULTADOS POR FASE
================================================== */
function mostrarResultadosFase(result: any) {

    document.getElementById("phases-panel")!.classList.remove("hidden");

    // ============ PREFLOP ============
    document.getElementById("preflop-hand-text")!.textContent = result.preflop.mano;
    document.getElementById("preflop-category")!.textContent = result.preflop.categoria;
    document.getElementById("preflop-equity")!.textContent = result.preflop.equity + "%";
    document.getElementById("preflop-rec")!.textContent = result.preflop.recomendacion;

    // ============ FLOP ============
    document.getElementById("flop-cards")!.textContent = result.flop.cartas.join(", ");
    document.getElementById("flop-category")!.textContent = result.flop.categoria;
    document.getElementById("flop-equity")!.textContent = result.flop.equity + "%";
    document.getElementById("flop-outs-count")!.textContent = result.flop.outs;
    document.getElementById("flop-outs-list")!.textContent =
        result.flop.outs_list.length ? result.flop.outs_list.join(", ") : "-";
    document.getElementById("flop-rec")!.textContent = result.flop.recomendacion;

    // ============ TURN ============
    document.getElementById("turn-card")!.textContent = result.turn.carta;
    document.getElementById("turn-category")!.textContent = result.turn.categoria;
    document.getElementById("turn-equity")!.textContent = result.turn.equity + "%";
    document.getElementById("turn-outs-count")!.textContent = result.turn.outs;
    document.getElementById("turn-outs-list")!.textContent =
        result.turn.outs_list.length ? result.turn.outs_list.join(", ") : "-";
    document.getElementById("turn-rec")!.textContent = result.turn.recomendacion;

    // ============ RIVER ============
    document.getElementById("river-card")!.textContent = result.river.carta;
    document.getElementById("river-category")!.textContent = result.river.categoria;
    document.getElementById("river-equity")!.textContent = result.river.equity + "%";
    document.getElementById("river-rec")!.textContent = result.river.recomendacion;

    // CONTEXTO
    document.getElementById("posicion-analizada")!.textContent = result.posicion;
    document.getElementById("final-cards")!.textContent =
        result.cartas_finales ? result.cartas_finales.join(", ") : "-";

    // NUEVO: ANÁLISIS GENERAL + RECOMENDACIÓN FINAL
    document.getElementById("resumen-general")!.textContent =
        result.analisis_general || "No disponible";

    document.getElementById("recomendacion-final")!.textContent =
        result.recomendacion_final || "No disponible";

    // Gráfico
    dibujarGraficoEvolucion(result.equity_evolucion);
}

/* ==================================================
   GRÁFICOS DEL DASHBOARD
================================================== */
function renderDynamicChart(chartData: any, type: string) {
    const ctx = document.getElementById("chart-canvas") as HTMLCanvasElement;

    if (dynamicChart) dynamicChart.destroy();

    dynamicChart = new Chart(ctx, {
        type,
        data: chartData.data,
        options: chartData.options
    });
}

async function cargarGraficoSeleccionado() {
    const tipo = (document.getElementById("chart-chooser") as HTMLSelectElement).value;
    let data;

    if (tipo === "winrate-posicion") data = await obtenerWinratePosicion();
    else if (tipo === "histograma-botes") data = await obtenerHistogramaBotes();
    else if (tipo === "agresividad-profit") data = await obtenerAgresividadProfit();
    else if (tipo === "frecuencia-categorias") data = await obtenerFrecuenciaCategorias();
    else if (tipo === "riesgo-winrate") data = await obtenerRiesgoWinrate();
    else if (tipo === "bote-agresividad") data = await obtenerBoteAgresividad();
    else data = await obtenerTimelineProfit();

    renderDynamicChart(data.chart, data.tipo);
}

/* ==================================================
   EVENTOS PRINCIPALES
================================================== */
document.addEventListener("DOMContentLoaded", () => {

    statsDiv = document.getElementById("estadisticas")!;
    errorPanel = document.getElementById("error-panel")!;

    cargarEstadisticas();
    cargarGraficoSeleccionado();

    document.getElementById("generar-dataset")!
        .addEventListener("click", async () => {
            await generarDataset();
            await cargarEstadisticas();
            await cargarGraficoSeleccionado();
        });

    const form = document.getElementById("hand-form") as HTMLFormElement;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const carta1 =
            (document.getElementById("rank1") as HTMLSelectElement).value +
            (document.getElementById("suit1") as HTMLSelectElement).value;

        const carta2 =
            (document.getElementById("rank2") as HTMLSelectElement).value +
            (document.getElementById("suit2") as HTMLSelectElement).value;

        const posicion =
            (document.getElementById("posicion") as HTMLSelectElement).value;

        const result = await analizarMano({
            cartas_usuario: [carta1, carta2],
            posicion
        });

        mostrarResultadosFase(result);
    });

    document.getElementById("chart-chooser")!
        .addEventListener("change", cargarGraficoSeleccionado);
});
