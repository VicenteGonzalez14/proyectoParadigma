# PreFlopData 

## Objetivo

PreFlopData es una aplicación web completa para el análisis de datos de póker Texas Hold’em, integrando un backend en Python/Flask y un frontend en HTML + TypeScript.
Esta entrega final incluye:

Aplicación web operativa y funcional

Integración total entre frontend y backend

Visualización gráfica dinámica

Análisis de manos fase por fase

Uso de múltiples paradigmas de programación

Código modular, mantenible y documentado

Manual de usuario y documentación técnica

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

## 🧠 Paradigmas de Programación Aplicados

### ✔️ Imperativo
Presente en:

- Rutas Flask  
- Control de flujo  
- Manipulación del DOM  
- Renderizado dinámico de gráficos  

---

### ✔️ Funcional
Funciones puras y reutilizables:

- `equity()`  
- `outs()`  
- `evaluar_mano_total()`  
- Procesos estadísticos en `stats.py`

---

### ✔️ Modular (estilo POO)
Aunque no se usan clases, se aplican principios POO:

- Organización modular  
- Separación de responsabilidades  
- Módulos reutilizables y escalables  

---

## Requisitos Previos

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

## Pasos para Ejecutar el Proyecto

### 1. Iniciar el Backend

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

## 2. Preparar el Frontend

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

## 3. Visualizar la Página Web

Abrir el archivo index.html con un navegador o con la extensión Live Server en Visual Studio Code.

Asegúrate de que el backend esté corriendo en el puerto 5000 antes de recargar la página.

   Si aparece el mensaje:

   “No se pudo conectar con el backend”

Verifica que Flask esté ejecutándose correctamente y que no haya cambiado el puerto.


## Se recomienda mantener este flujo de ejecución:

1️⃣ Iniciar backend → 2️⃣ Compilar frontend → 3️⃣ Visualizar página.

## 📘 Manual de Usuario
✔️ Generar dataset

Desde la interfaz, presionar:

```bash
[ Generar nuevo dataset ]
```

Esto produce un nuevo archivo poker_dataset.json con miles de manos simuladas.

### ✔️ Ver estadísticas generales

El panel muestra:

- Total de manos  
- Ganadas / Perdidas  
- Winrate  
- Agresividad media  
- Riesgo medio  
- Profit neto  
- Bote promedio  

Todos los valores son calculados y enviados por el backend.

---

### ✔️ Analizador de mano por fases

1. Selecciona tus dos cartas  
2. Elige tu posición  
3. Presiona **Analizar Mano por Fases**

El backend simula automáticamente:

- **Flop**
- **Turn**
- **River**

Y entrega:

- Categoría por fase  
- Equity por fase  
- Outs  
- Cartas que mejoran  
- Recomendación por fase  
- Análisis general  
- Recomendación final  
- Gráfico de evolución de equity  

---

### ✔️ Visualizaciones (Dashboard)

Incluye gráficos de:

- Winrate por posición  
- Histogramas de botes  
- Agresividad vs Winrate  
- Frecuencia de categorías  
- Riesgo vs Winrate  
- Bote promedio según agresividad  
- Profit acumulado  

Todos generados dinámicamente con **Chart.js**.

---

## 📊 Procesamiento en Backend

El backend realiza:

- Simulación de mazos  
- Cálculo de Equity (Monte Carlo)  
- Evaluación automática de manos  
- Cálculo de outs  
- Estadísticas agrupadas con **Pandas**  
- Exposición de **API REST**  

---

## 🔗 Integración Frontend + Backend

Rutas REST principales:

```bash
/api/generar
/api/estadisticas
/api/analizar-fases
/api/charts/*
```

Toda la comunicación es manejada desde `api.ts` usando **fetch()**.

---

## 🧹 Modularidad y Limpieza

### Backend
- Módulos separados: **generación**, **proceso**, **estadísticas**  
- Código documentado  
- Estructura clara y extensible  

### Frontend
- `api.ts` → capa de servicios REST  
- `main.ts` → controlador de interfaz  
- HTML organizado  
- CSS limpio y responsivo  

---

## 🧾 Repositorio y Gestión del Código

- Repositorio actualizado  
- Incluye EP1, EP2 y entrega final  
- Commits descriptivos  
- Separación clara entre frontend y backend  

---

## 👥 Autores

- **Gaspar Albornoz**  
- **Ramón Espinoza**  
- **Vicente González**
