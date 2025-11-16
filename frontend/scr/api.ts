const API_BASE = "http://127.0.0.1:5000/api";

export async function obtenerEstadisticas(): Promise<any> {
    const resp = await fetch(`${API_BASE}/estadisticas`);
    if (!resp.ok) throw new Error("No se pudo conectar con el backend");
    return await resp.json();
}

export async function generarDataset(): Promise<any> {
    const resp = await fetch(`${API_BASE}/generar`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({num_manos: 5000})
    });
    if (!resp.ok) throw new Error("No se pudo generar dataset");
    return await resp.json();
}

export async function analizarMano(cartas_usuario: string[], cartas_comunitarias: string[]): Promise<any> {

    const payload = {
        cartas_usuario: cartas_usuario,
        cartas_comunitarias: cartas_comunitarias,
        n_rivales: 3 // Podrías añadir un input para esto luego
    };

    const resp = await fetch(`${API_BASE}/analizar`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    // Manejo de errores mejorado
    if (!resp.ok) {
        const errData = await resp.json(); // Lee el error que envía el backend
        throw new Error(errData.error || "No se pudo analizar la mano");
    }
    return await resp.json();
}