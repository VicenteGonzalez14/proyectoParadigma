// 1. IMPORTACIONES
// Importa las funciones de tu API
import { obtenerEstadisticas, generarDataset, analizarMano } from "./api.js";
import { Chart, registerables, type TooltipItem } from 'chart.js';
Chart.register(...registerables);


// --- Panel de Estadísticas (El que ya tenías) ---
const statsDiv = document.getElementById("estadisticas")!;
const loadingText = document.getElementById("loading-text")!;
const errorPanel = document.getElementById("error-panel")!;
const generarBtn = document.getElementById("generar-dataset")!;

// --- Panel Interactivo (El nuevo) ---
const handForm = document.getElementById("hand-form") as HTMLFormElement;
const chartPanel = document.getElementById("chart-panel")!;
const chartTitle = document.getElementById("chart-title")!;
const analysisCategory = document.getElementById("analysis-category")!;
const chartCanvas = document.getElementById("win-probability-chart") as HTMLCanvasElement;

// ===================================================
// 3. VARIABLES GLOBALES
// ===================================================

// Variable para guardar la instancia del gráfico y poder actualizarla
let winChart: Chart | null = null;

// ===================================================
// 4. FUNCIONES DE ESTADÍSTICAS (Tu código original)
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
  // Ocultamos las stats y el loading si hay un error
  statsDiv.innerHTML = '';
  loadingText.style.display = "none"; 
  errorPanel.querySelector("p")!.textContent = msg;
}

async function cargarEstadisticas() {
  try {
    const data = await obtenerEstadisticas();
    mostrarEstadisticas(data);
  } catch (e: any) {
    mostrarError("No se pudo conectar con el backend.");
  }
}

// Botón para generar dataset
generarBtn.addEventListener("click", async () => {
  const generarBtn = document.getElementById("generar-dataset") as HTMLButtonElement;

  generarBtn.textContent = "Generando...";
  generarBtn.disabled = true; // Deshabilitar mientras genera
  try {
    await generarDataset();
    await cargarEstadisticas(); // Recarga las stats después de generar
    generarBtn.textContent = "Generar nuevo dataset";
  } catch (e) {
    mostrarError("No se pudo generar el dataset.");
  }
  generarBtn.disabled = false; // Vuelve a habilitar
});

// ===================================================
// 5. NUEVAS FUNCIONES (La parte interactiva que faltaba)
// ===================================================

/**
 * Dibuja o actualiza el gráfico de dona con los nuevos datos.
 */
function dibujarGrafico(analysisData: any) {
  chartPanel.classList.remove("hidden"); // Muestra el panel del gráfico

  // Actualiza los textos
  const cartasStr = analysisData.cartas_analizadas.join(", ");
  chartTitle.textContent = `Análisis: ${cartasStr}`;
  analysisCategory.textContent = `Categoría de Mano: ${analysisData.categoria_mano}`;

  const ctx = chartCanvas.getContext("2d");
  if (!ctx) return;

  const data = {
    labels: [ 'Prob. Victoria', 'Prob. Derrota' ],
    datasets: [{
      data: [
        analysisData.probabilidad_victoria, 
        analysisData.probabilidad_derrota
      ],
      backgroundColor: [ '#20b6c8', '#CC3333' ], // Azul (tu color) y Rojo
      hoverOffset: 4
    }]
  };

  // Si el gráfico ya existe, lo actualizamos (para no crear uno nuevo)
  if (winChart) {
    winChart.data = data;
    winChart.update();
  } else {
    // Si es la primera vez, lo creamos
    winChart = new Chart(ctx, {
      type: 'doughnut', // Gráfico de dona
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: function(context: TooltipItem<"doughnut">) {
                return `${context.label}: ${context.raw}%`;
                }
            }
          }
        }
      }
    });
  }
}

/**
 * Manejador del envío del formulario de análisis
 */
handForm.addEventListener("submit", async (e) => {
  e.preventDefault(); // ¡Evita que la página se recargue!

  const btn = handForm.querySelector("button")!;
  btn.textContent = "Analizando...";
  btn.disabled = true;
  errorPanel.classList.add("hidden"); // Oculta errores viejos

  try {
    // 1. Recolectar datos del formulario
    const cartas_usuario = [
      (document.getElementById("carta1") as HTMLInputElement).value,
      (document.getElementById("carta2") as HTMLInputElement).value
    ];
    
    // Recolecta las 5 cartas de la mesa (si están vacías, las filtra)
    const cartas_comunitarias = [
      (document.getElementById("com1") as HTMLInputElement).value,
      (document.getElementById("com2") as HTMLInputElement).value,
      (document.getElementById("com3") as HTMLInputElement).value,
      (document.getElementById("com4") as HTMLInputElement).value,
      (document.getElementById("com5") as HTMLInputElement).value
    ].filter(c => c.trim() !== ""); // Filtra inputs vacíos

    // 2. Enviar a la API de análisis
    const resultado = await analizarMano(cartas_usuario, cartas_comunitarias);
    
    // 3. Dibujar el gráfico con la respuesta
    dibujarGrafico(resultado);

  } catch (e: any) {
    // 4. Mostrar error si algo falla
    mostrarError(e.message || "Error desconocido al analizar.");
    chartPanel.classList.add("hidden"); // Oculta el gráfico si hay error
  }

  btn.textContent = "Analizar Mano";
  btn.disabled = false;
});

// ===================================================
// 6. CARGA INICIAL
// ===================================================

// Carga las estadísticas generales al abrir la página
cargarEstadisticas();