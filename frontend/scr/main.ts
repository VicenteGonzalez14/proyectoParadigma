import { obtenerEstadisticas, generarDataset } from "./api.js";

const statsDiv = document.getElementById("estadisticas")!;
const loadingText = document.getElementById("loading-text")!;
const errorPanel = document.getElementById("error-panel")!;
const generarBtn = document.getElementById("generar-dataset")!;

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
    loadingText.textContent = "Cargando estadísticas...";
    errorPanel.querySelector("p")!.textContent = msg;
}

// Inicializa al cargar
async function cargarEstadisticas() {
    try {
        const data = await obtenerEstadisticas();
        mostrarEstadisticas(data);
    } catch (e: any) {
        mostrarError("No se pudo conectar con el backend.");
    }
}

// Botón para generar dataset desde frontend
generarBtn.addEventListener("click", async () => {
    const generarBtn = document.getElementById("generar-dataset") as HTMLButtonElement;

    generarBtn.textContent = "Generando...";
    try {
        await generarDataset();
        await cargarEstadisticas();
        generarBtn.textContent = "Generar nuevo dataset";
    } catch (e) {
        mostrarError("No se pudo generar el dataset.");
    }
    generarBtn.disabled = false;
});

// Carga inicial
cargarEstadisticas();
