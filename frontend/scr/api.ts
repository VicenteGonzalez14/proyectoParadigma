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
