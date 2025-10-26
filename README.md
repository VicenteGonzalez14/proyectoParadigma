# 🃏 PreFlopData – Entrega Parcial 2

## 🎯 Objetivo

Este proyecto implementa una versión intermedia operativa del sistema **PreFlopData**, una aplicación web para el análisis de datos de póker **Texas Hold’em**.  
En esta etapa se demuestra la conexión real **Frontend ↔ Backend**, la **generación y manipulación de datos simulados** y la **validación de entradas y salidas reales**.

- **Backend (Flask + Python):** genera, procesa y devuelve estadísticas de un dataset simulado de póker.
- **Frontend (HTML + TypeScript + CSS):** permite visualizar los resultados y estadísticas obtenidas desde el backend.

---

## ⚙️ Estructura del Proyecto

```text
proyectoParadigma/
├── backend/
│   ├── app.py
│   ├── utils/
│   │   ├── generator.py
│   │   ├── process.py
│   │   └── stats.py
│   ├── data/
│   │   └── poker_dataset.json
│   ├── requirements.txt
│   └── venv/  (entorno virtual local)
│
├── frontend/
│   ├── scr/
│   │   ├── api.ts
│   │   └── main.ts
│   ├── dist/        (carpeta generada al compilar TypeScript)
│   ├── index.html
│   ├── style.css
│   ├── package.json
│   ├── tsconfig.json
│   └── scripts.js   (reservado para futuras integraciones en EP3)
│
└── README.md
│
│
└── Otros (en esta carpeta se encuentra el EP1, ya que al momento de informar para realizar otro branch ya habiamos modificado el anterior)
```
---

## 🧩 Requisitos Previos

### 🔹 Backend
Asegúrate de tener instalado:
- **Python 3.10 o superior**
- **Flask**
- **Pandas**
- **flask-cors**
- **python-dotenv**

Estas dependencias están listadas en `requirements.txt`.

### 🔹 Frontend
- **Node.js** (v16 o superior)
- **TypeScript** (instalado localmente con npm)

---

## 🚀 Pasos para Ejecutar el Proyecto

### 🧱 1. Iniciar el Backend

1. Abrir una terminal en la carpeta `backend/`.
   
2. Activar el entorno virtual:
   ```bash
   venv\Scripts\activate
   ```
   
3. Instalar dependencias (solo la primera vez):
   ``` bash
   pip install -r requirements.txt
   ```
   
4. Ejecutar Flask:
   ```bash
   python app.py
   ```
 
5. El servidor quedará disponible en:

   ```cpp
   http://127.0.0.1:5000
   ```
   
6. Si todo está correcto, verás en la consola:

   ```csharp
    * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
   ```

## 💻 2. Preparar el Frontend

Abrir una nueva terminal en la carpeta frontend/.

1. Inicializar el entorno de Node (solo la primera vez):

   ```bash
   npm init -y
   ```

2. Instalar TypeScript:

   ```bash
   npm install -D typescript
   ```

3. Crear y configurar el archivo tsconfig.json (solo si no existe):

   ```bash
   npx tsc --init
   ```
   
4. Luego verificar que la configuración sea exactamente igual a la siguiente:

   ``` json
   {
     "compilerOptions": {
       "target": "ES2020",
       "module": "ESNext",
       "moduleResolution": "Bundler",
       "strict": true,
       "skipLibCheck": true,
       "rootDir": "./scr",
       "outDir": "./dist",
       "sourceMap": false,
       "removeComments": true,
       "noEmitOnError": true,
       "allowJs": false,
       "esModuleInterop": true,
       "forceConsistentCasingInFileNames": true
     },
     "include": ["scr"],
     "exclude": ["node_modules", "dist"]
   }

   ```
5. Compilar el código TypeScript:

   ```bash
   npx tsc
   ```
   
Esto creará automáticamente la carpeta dist/ con los archivos .js compilados.

## 🌐 3. Visualizar la Página Web

Abrir el archivo index.html con un navegador o con la extensión Live Server en Visual Studio Code.

Asegúrate de que el backend esté corriendo en el puerto 5000 antes de recargar la página.

💡 Si aparece el mensaje:

   “No se pudo conectar con el backend”

Verifica que Flask esté ejecutándose correctamente y que no haya cambiado el puerto.

# 📊 Validación de Resultados

Al abrir la página, se mostrarán las estadísticas obtenidas dinámicamente desde el backend:

   ```text
   Total de manos generadas

   Manos ganadas y perdidas

   Porcentaje de victoria

   Bote promedio

   Agresividad media

   Riesgo medio
   ```

Estos datos se leen directamente desde el dataset poker_dataset.json generado por el backend Flask.

## 🧠 Notas Técnicas

El proyecto aplica los paradigmas POO, Funcional e Imperativo.

La comunicación entre capas utiliza el formato REST + JSON sobre el protocolo HTTP.

El archivo scripts.js no se usa en esta entrega, pero se reserva para futuras extensiones visuales (por ejemplo, integración con Chart.js en la EP3).

## Se recomienda mantener este flujo de ejecución:

1️⃣ Iniciar backend → 2️⃣ Compilar frontend → 3️⃣ Visualizar página.

✨ Créditos
- Gaspar Albornoz
- Ramon Espinoza
- Vicente González.
