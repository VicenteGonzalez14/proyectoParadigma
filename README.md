# 🃏 PreFlopData – Entrega Parcial 2

## 🎯 Objetivo
Este proyecto simula un sistema de análisis de datos de póker **Texas Hold'em**, donde:
- El **backend (Flask + Python)** genera y procesa un dataset simulado.  
- El **frontend (HTML + TypeScript + CSS)** visualiza estadísticas básicas.  

Esta entrega demuestra:
- Conexión real **frontend ↔ backend**  
- Procesamiento y manipulación de datos reales  
- Validación de entradas/salidas  

---

## ⚙️ Estructura del proyecto

proyectoParadigma/
├── backend/
│ ├── app.py
│ ├── utils/
│ │ ├── generator.py
│ │ ├── process.py
│ │ └── stats.py
│ ├── data/
│ │ └── poker_dataset.json
│ └── requirements.txt
│
├── frontend/
│ ├── scr/
│ │ ├── api.ts
│ │ └── main.ts
│ ├── dist/ (generado al compilar)
│ ├── index.html
│ ├── style.css
│ ├── package.json
│ └── tsconfig.json
│
└── README.md


---

## 🧩 Requisitos previos

### 🔹 Backend
- Python 3.10 o superior  
- Flask  
- Pandas  
- flask-cors  
- python-dotenv  

*(todo está incluido en `requirements.txt`)*

### 🔹 Frontend
- Node.js instalado (v16+ recomendado)
- TypeScript (instalado localmente con npm)

---

## 🚀 Pasos para ejecutar el proyecto

### 🧱 1. Iniciar el backend

1. Abrir una terminal en la carpeta `backend/`.  
2. Activar el entorno virtual:
   ```bash
   venv\Scripts\activate
   ```
3. Instalar dependencias (solo la primera vez):
  ```bash
  pip install -r requirements.txt
  ```

4. Ejecutar Flask:
  ```bash
  python app.py
  ```
5. El backend quedará disponible en:
  ```ccp
  http://127.0.0.1:5000
  ```

✅ Si todo está correcto, verás un mensaje en consola como:
```bash
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

2. Preparar el frontend

1. Abrir una nueva terminal en la carpeta frontend/.

2. Inicializar Node (solo una vez):
   ```bash
   npm init -y
   ```

3. Instalar TypeScript:
  ```bash
  npm install -D typescript
  ```
4. Verificar que existe el archivo tsconfig.json con la configuración estándar del proyecto

5. Compilar el código TypeScript:
  ```bash
  npx tsc
  ```
Esto creará automáticamente la carpeta dist/ con los archivos .js generados.

3. Visualizar la página web

Abrir el archivo index.html con el navegador o usando la extensión Live Server en Visual Studio Code.

Si el backend está activo, la página mostrará los datos reales del archivo poker_dataset.json.

💡 Si aparece un mensaje de error (“No se pudo conectar con el backend”), asegúrate de que Flask esté ejecutándose en el puerto correcto.

📊 Validación de resultados

Al abrir la página, se mostrarán:

Total de manos generadas

Manos ganadas y perdidas

Porcentaje de victoria

Bote promedio

Agresividad y riesgo medios

Todos estos datos son obtenidos dinámicamente desde el backend.
