# ⚽ Interactive Scouting Report — UCL Final 2019

Aplicación interactiva de análisis de rendimiento para la Final de la UEFA Champions League 2019 entre Liverpool y Tottenham Hotspur. Selecciona cualquier jugador del partido y visualiza sus estadísticas en tiempo real.

## 🔗 Demo en vivo
👉 [Abrir aplicación](https://interactivescoutingreport1-ddgbxquka6x4sj5u8zyteg.streamlit.app/)

---

## Visualizaciones por jugador

- **Mapa de calor** — zonas de mayor presencia en el campo
- **Mapa de pases** — pases completados (verde) vs fallados (rojo) con dirección
- **Mapa de tiros** — ubicación, xG y goles
- **Stats resumen** — toques, pases, tiros, goles, xG, duelos, presiones y recuperaciones

---

## Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat)
![StatsBomb](https://img.shields.io/badge/StatsBomb-Open%20Data-1DB954?style=flat)
![mplsoccer](https://img.shields.io/badge/mplsoccer-0.0.1-blue?style=flat)

---

## Estructura del repositorio
interactive_scouting_report_1/
│
├── report_ucl_final_2019_stl.py                  # Aplicación principal Streamlit
├── requirements.txt        # Dependencias
└── README.md

---

## Cómo ejecutar localmente

```bash
git clone https://github.com/dagovas27/interactive_scouting_report_1.git
cd interactive_scouting_report_1
pip install -r requirements.txt
streamlit run app.py
```

---

## Datos

Los datos provienen de **StatsBomb Open Data** — eventos detallados por jugador incluyendo ubicación, tipo de acción, xG y más.

---

## Autor

**Daniel Vásquez** — [@dagovas27](https://github.com/dagovas27)
Universidad Pontificia Bolivariana — Ingeniería en Ciencia de Datos
