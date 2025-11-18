// ===============================
// CHART.JS VIENE DESDE CDN
// ===============================
declare const Chart: any;


// ========================================
// 1. IMPORTACIONES DESDE API.JS
// ========================================
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


// ===================================================
// 3. DECLARACIÓN DE VARIABLES GLOBALES
// ===================================================

// --- Referencias al DOM ---
let statsDiv: HTMLElement;
let loadingText: HTMLElement;
let errorPanel: HTMLElement;
let generarBtn: HTMLButtonElement; 
let handForm: HTMLFormElement;
let chartPanel: HTMLElement;
let chartTitle: HTMLElement;
let analysisCategory: HTMLElement;
let winProbabilityChartCanvas: HTMLCanvasElement;
let errorChartsPanel: HTMLElement;
let chartWinratePosicionCanvas: HTMLCanvasElement;
let chartHistogramaBotesCanvas: HTMLCanvasElement;
let chartAgresividadProfitCanvas: HTMLCanvasElement;
let chartFrecuenciaCategoriasCanvas: HTMLCanvasElement;
let chartRiesgoWinrateCanvas: HTMLCanvasElement;
let chartBoteAgresividadCanvas: HTMLCanvasElement;
let chartTimelineProfitCanvas: HTMLCanvasElement;

// --- Cache de Gráficos ---
let winChart: any = null;

let dashboardCharts: { [key: string]: any | null } = {
    'winrate-posicion': null, 
    'histograma-botes': null, 
    'agresividad-profit': null,
    'frecuencia-categorias': null, 
    'riesgo-winrate': null, 
    'bote-agresividad': null, 
    'timeline-profit': null,
};


// ===================================================
// 4. FUNCIONES DE ESTADÍSTICAS Y ERRORES
// ===================================================

function mostrarEstadisticas(data: any) {
    statsDiv.innerHTML = `
    <ul>
        <li><strong>Total de manos:</strong> ${data.total_manos}</li>
        <li><strong>Manos ganadas:</strong> ${data.ganadas}</li>
        <li><strong>Manos perdidas:</strong> ${data.perdidas}</li>
        <li><strong>Tasa de victoria:</strong> ${data.tasa_victoria}%</li>
        <li><strong>Bote promedio:</strong> ${data.bote_promedio}</li>
        <li><strong>Agresividad media:</strong> ${data.agresividad_media}</li>
        <li><strong>Riesgo medio:</strong> ${data.riesgo_medio}</li>
    </ul>
    `;
    loadingText.style.display = "none";
    errorPanel.classList.add("hidden");
}

function mostrarError(msg: string) {
    errorPanel.classList.remove("hidden");
    statsDiv.innerHTML = '';
    loadingText.style.display = "none"; 
    errorPanel.querySelector("p")!.textContent = msg;
}

async function cargarEstadisticas() {
    try {
      const data = await obtenerEstadisticas();
      mostrarEstadisticas(data);
    } catch (e: any) {
      mostrarError("No se pudo conectar con el backend. (Verifique el servidor Flask)");
    }
}


// ===================================================
// 5. FUNCIONES DE ANÁLISIS DE MANO
// ===================================================

function dibujarGrafico(analysisData: any) {
    chartPanel.classList.remove("hidden");

    const cartasStr = analysisData.cartas_analizadas.join(", ");
    chartTitle.textContent = `Análisis: ${cartasStr}`;
    analysisCategory.textContent = `Categoría de Mano: ${analysisData.categoria_mano}`;

    const ctx = winProbabilityChartCanvas.getContext("2d");
    if (!ctx) return;

    const data = {
      labels: [ 'Prob. Victoria', 'Prob. Derrota' ],
      datasets: [{
        data: [
          analysisData.probabilidad_victoria, 
          analysisData.probabilidad_derrota
        ],
        backgroundColor: [ '#20b6c8', '#CC3333' ],
        hoverOffset: 4
      }]
    };

    if (winChart) {
      winChart.data = data;
      winChart.update();
    } else {
      winChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            tooltip: {
              callbacks: {
                label: function(context: any) {
                  return `${context.label}: ${context.raw}%`;
                  }
              }
            }
          }
        }
      });
    }
}


// ===================================================
// 6. DASHBOARD DE GRÁFICOS
// ===================================================

function updateChart(chartId: string, canvas: HTMLCanvasElement, chartType: string, data: any, options: any) {
    if (dashboardCharts[chartId]) {
        dashboardCharts[chartId]!.data = data;
        dashboardCharts[chartId]!.options = options;
        dashboardCharts[chartId]!.update();
    } else {
        const ctx = canvas.getContext("2d");
        if (ctx) {
            dashboardCharts[chartId] = new Chart(ctx, { type: chartType as any, data, options });
        }
    }
}

async function cargarWinratePosicion() {
    try {
        const data = await obtenerWinratePosicion();
        const chartData = {
            labels: data.map((d: any) => `Jugadores: ${d.posicion}`),
            datasets: [
                {
                    label: 'Winrate (%)',
                    data: data.map((d: any) => d.winrate),
                    backgroundColor: 'rgba(32, 182, 200, 0.7)',
                    yAxisID: 'y'
                },
                {
                    label: 'Manos Jugadas (Count)',
                    data: data.map((d: any) => d.hands),
                    backgroundColor: 'rgba(255, 159, 64, 0.7)',
                    type: 'line',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    yAxisID: 'y1'
                }
            ]
        };

        const options = {
            responsive: true,
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Winrate (%)' } },
                y1: { 
                    type: 'linear' as const, 
                    display: true, 
                    position: 'right' as const, 
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: 'Manos Jugadas' } 
                }
            }
        };
        updateChart('winrate-posicion', chartWinratePosicionCanvas, 'bar', chartData, options);
    } catch (e) { console.error(e); }
}

async function cargarHistogramaBotes() {
    try {
        const data = await obtenerHistogramaBotes();
        const chartData = {
            labels: data.bins,
            datasets: [{
                label: 'Frecuencia de Manos',
                data: data.counts,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };

        const options = { responsive: true, scales: { y: { beginAtZero: true } } };
        updateChart('histograma-botes', chartHistogramaBotesCanvas, 'bar', chartData, options);
    } catch (e) { console.error(e); }
}

async function cargarAgresividadProfit() {
    try {
        const data = await obtenerAgresividadProfit();
        const chartData = {
            labels: data.map((d: any) => d.label),
            datasets: [{
                label: 'Winrate Promedio (%)',
                data: data.map((d: any) => d.winrate_promedio),
                backgroundColor: 'rgba(153, 102, 255, 0.7)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        };

        const options = { 
            responsive: true, 
            scales: { 
                y: { beginAtZero: true, title: { display: true, text: 'Winrate (%)' } } 
            },
            plugins: {
                tooltip: { 
                    callbacks: { 
                        label: (context: any) => `${context.dataset.label}: ${context.parsed.y}%` 
                    } 
                }
            }
        };
        updateChart('agresividad-profit', chartAgresividadProfitCanvas, 'bar', chartData, options);
    } catch (e) { console.error(e); }
}

async function cargarFrecuenciaCategorias() {
    try {
        const data = await obtenerFrecuenciaCategorias();
        const chartData = {
            labels: data.map((d: any) => d.categoria),
            datasets: [{
                label: 'Cantidad',
                data: data.map((d: any) => d.cantidad),
                backgroundColor: [
                    '#20b6c8', '#FF6384', '#FF9F40', '#4BC0C0', 
                    '#9966FF', '#FFCD56', '#C9CBCE', '#36A2EB'
                ],
                hoverOffset: 4
            }]
        };

        const options = { responsive: true };
        updateChart('frecuencia-categorias', chartFrecuenciaCategoriasCanvas, 'pie', chartData, options);
    } catch (e) { console.error(e); }
}

async function cargarRiesgoWinrate() {
    try {
        const data = await obtenerRiesgoWinrate();
        const chartData = {
            labels: data.map((d: any) => d.label),
            datasets: [{
                label: 'Winrate Promedio (%)',
                data: data.map((d: any) => d.winrate_promedio),
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        };

        const options = { 
            responsive: true, 
            scales: { 
                y: { beginAtZero: true, title: { display: true, text: 'Winrate (%)' } } 
            },
            plugins: {
                tooltip: { 
                    callbacks: { 
                        label: (context: any) => `${context.dataset.label}: ${context.parsed.y}%` 
                    } 
                }
            }
        };
        updateChart('riesgo-winrate', chartRiesgoWinrateCanvas, 'bar', chartData, options);
    } catch (e) { console.error(e); }
}

async function cargarBoteAgresividad() {
    try {
        const data = await obtenerBoteAgresividad();
        const chartData = {
            labels: data.map((d: any) => d.label),
            datasets: [{
                label: 'Bote Promedio',
                data: data.map((d: any) => d.bote_promedio),
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };

        const options = { 
            responsive: true, 
            scales: { 
                y: { beginAtZero: true, title: { display: true, text: 'Bote Promedio' } } 
            }
        };
        updateChart('bote-agresividad', chartBoteAgresividadCanvas, 'bar', chartData, options);
    } catch (e) { console.error(e); }
}

async function cargarTimelineProfit() {
    try {
        const data = await obtenerTimelineProfit();
        const chartData = {
            labels: data.mano_id,
            datasets: [{
                label: 'Profit Acumulado',
                data: data.profit_acumulado,
                borderColor: '#4BC0C0',
                tension: 0.1,
                fill: false
            }]
        };

        const options = { 
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Número de Mano' } },
                y: { title: { display: true, text: 'Profit Acumulado (Unidades)' } }
            }
        };
        updateChart('timeline-profit', chartTimelineProfitCanvas, 'line', chartData, options);
    } catch (e) { console.error(e); }
}


async function cargarDashboard() {
    errorChartsPanel.classList.add("hidden");
    try {
        await Promise.all([
            cargarWinratePosicion(),
            cargarHistogramaBotes(),
            cargarAgresividadProfit(),
            cargarFrecuenciaCategorias(),
            cargarRiesgoWinrate(),
            cargarBoteAgresividad(),
            cargarTimelineProfit(),
        ]);
        console.log("✅ Dashboard de gráficos cargado.");
    } catch (error) {
        errorChartsPanel.classList.remove("hidden");
        console.error("Fallo al cargar el dashboard:", error);
    }
}


// ===================================================
// 7. CARGA INICIAL Y LISTENERS
// ===================================================

async function iniciarApp() {
    await cargarEstadisticas();
    if (errorPanel.classList.contains("hidden")) {
        await cargarDashboard();
    }
}


document.addEventListener("DOMContentLoaded", () => {

    statsDiv = document.getElementById("estadisticas")!;
    loadingText = document.getElementById("loading-text")!;
    errorPanel = document.getElementById("error-panel")!;
    generarBtn = document.getElementById("generar-dataset") as HTMLButtonElement; 

    handForm = document.getElementById("hand-form") as HTMLFormElement; 
    chartPanel = document.getElementById("chart-panel")!;
    chartTitle = document.getElementById("chart-title")!;
    analysisCategory = document.getElementById("analysis-category")!;
    winProbabilityChartCanvas = document.getElementById("win-probability-chart") as HTMLCanvasElement;

    errorChartsPanel = document.getElementById("error-charts-panel")!;
    chartWinratePosicionCanvas = document.getElementById("chart-winrate-posicion") as HTMLCanvasElement;
    chartHistogramaBotesCanvas = document.getElementById("chart-histograma-botes") as HTMLCanvasElement;
    chartAgresividadProfitCanvas = document.getElementById("chart-agresividad-profit") as HTMLCanvasElement; 
    chartFrecuenciaCategoriasCanvas = document.getElementById("chart-frecuencia-categorias") as HTMLCanvasElement;
    chartRiesgoWinrateCanvas = document.getElementById("chart-riesgo-winrate") as HTMLCanvasElement;
    chartBoteAgresividadCanvas = document.getElementById("chart-bote-agresividad") as HTMLCanvasElement;
    chartTimelineProfitCanvas = document.getElementById("chart-timeline-profit") as HTMLCanvasElement;

    // ===================================================
    // LÓGICA DE INPUTS DE CARTAS (Ocultos)
    // ===================================================

    function updateCardValue(rankId: string, suitId: string, targetId: string) {
        const rankEl = document.getElementById(rankId) as HTMLSelectElement | null;
        const suitEl = document.getElementById(suitId) as HTMLSelectElement | null;
        const targetEl = document.getElementById(targetId) as HTMLInputElement | null;

        if (rankEl && suitEl && targetEl) {
            const rank = rankEl.value.trim();
            const suit = suitEl.value.trim();
            
            if (rank && suit) {
                targetEl.value = rank + suit;
            } else {
                targetEl.value = "";
            }
        }
    }

    const cardInputIds = ["carta1", "carta2", "com1", "com2", "com3", "com4", "com5"];

    cardInputIds.forEach(id => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.id = id;
        input.name = id;
        handForm.appendChild(input); 
    });

    const selectorsToListen = [
        { rank: 'rank1', suit: 'suit1', target: 'carta1' },
        { rank: 'rank2', suit: 'suit2', target: 'carta2' },
        { rank: 'com1_rank', suit: 'com1_suit', target: 'com1' },
        { rank: 'com2_rank', suit: 'com2_suit', target: 'com2' },
        { rank: 'com3_rank', suit: 'com3_suit', target: 'com3' },
        { rank: 'com4_rank', suit: 'com4_suit', target: 'com4' },
        { rank: 'com5_rank', suit: 'com5_suit', target: 'com5' },
    ];

    selectorsToListen.forEach(s => {
        document.getElementById(s.rank)?.addEventListener('change', () => updateCardValue(s.rank, s.suit, s.target));
        document.getElementById(s.suit)?.addEventListener('change', () => updateCardValue(s.rank, s.suit, s.target));
    });

    selectorsToListen
        .filter(s => s.target === 'carta1' || s.target === 'carta2')
        .forEach(s => updateCardValue(s.rank, s.suit, s.target));


    // ===================================================
    // EVENTOS
    // ===================================================

    generarBtn.addEventListener("click", async () => {
        generarBtn.textContent = "Generando...";
        generarBtn.disabled = true;
        try {
            await generarDataset();
            await cargarEstadisticas();
            await cargarDashboard();
            generarBtn.textContent = "Generar nuevo dataset";
        } catch (e) {
            mostrarError("No se pudo generar el dataset.");
        }
        generarBtn.disabled = false;
    });

    handForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const btn = handForm.querySelector("button")!;

        btn.textContent = "Analizando...";
        btn.disabled = true;
        errorPanel.classList.add("hidden");

        try {
            const cartas_usuario = [
                (document.getElementById("carta1") as HTMLInputElement).value,
                (document.getElementById("carta2") as HTMLInputElement).value
            ];
            
            const cartas_comunitarias = [
                (document.getElementById("com1") as HTMLInputElement).value,
                (document.getElementById("com2") as HTMLInputElement).value,
                (document.getElementById("com3") as HTMLInputElement).value,
                (document.getElementById("com4") as HTMLInputElement).value,
                (document.getElementById("com5") as HTMLInputElement).value
            ].filter(c => c.trim() !== "");

            const resultado = await analizarMano(cartas_usuario, cartas_comunitarias);
            dibujarGrafico(resultado);

        } catch (e: any) {
            mostrarError(e.message || "Error desconocido al analizar.");
            chartPanel.classList.add("hidden");
        }

        btn.textContent = "Analizar Mano";
        btn.disabled = false;
    });


    iniciarApp();
});