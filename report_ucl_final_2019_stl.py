import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from statsbombpy import sb
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Scouting Report — UCL Final 2019",
    page_icon="⚽",
    layout="wide"
)

# Estilos
st.markdown("""
<style>
    .main { background-color: #1a1a2e; }
    h1, h2, h3 { color: white; }
    .stSelectbox label { color: white; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align:center; color:white;'>⚽ Interactive Scouting Report</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#AAAAAA;'>UEFA Champions League Final 2019 · Liverpool vs Tottenham Hotspur</h3>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def cargar_datos():
    return sb.events(match_id=22912)

eventos = cargar_datos()

jugadores = eventos[['player', 'team']].dropna().drop_duplicates().sort_values('team')

# Selector
col1, col2 = st.columns([1, 2])
with col1:
    equipo_sel = st.selectbox("Selecciona el equipo", jugadores['team'].unique())
with col2:
    jugadores_equipo = jugadores[jugadores['team'] == equipo_sel]['player'].tolist()
    jugador_sel = st.selectbox("Selecciona el jugador", jugadores_equipo)

st.markdown("---")

# Funciones
def mapa_calor(eventos, jugador, ax):
    datos = eventos[eventos['player'] == jugador].copy()
    datos = datos[datos['location'].notna()]
    datos['x'] = datos['location'].apply(lambda l: l[0])
    datos['y'] = datos['location'].apply(lambda l: l[1])
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a2e', line_color='white')
    pitch.draw(ax=ax)
    if len(datos) > 5:
        pitch.kdeplot(datos['x'], datos['y'], ax=ax, cmap='YlOrRd', fill=True, alpha=0.7, levels=15)
    pitch.scatter(datos['x'], datos['y'], ax=ax, s=15, color='white', alpha=0.3, zorder=3)
    ax.set_title('Mapa de calor', color='white', fontsize=11, fontweight='bold')
    ax.set_facecolor('#1a1a2e')

def mapa_pases(eventos, jugador, ax):
    datos = eventos[(eventos['player'] == jugador) & (eventos['type'] == 'Pass')].copy()
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a2e', line_color='white')
    pitch.draw(ax=ax)
    if len(datos) == 0:
        ax.set_title('Sin pases', color='white', fontsize=11)
        ax.set_facecolor('#1a1a2e')
        return
    datos['x'] = datos['location'].apply(lambda l: l[0])
    datos['y'] = datos['location'].apply(lambda l: l[1])
    datos['x_end'] = datos['pass_end_location'].apply(lambda l: l[0] if isinstance(l, list) else None)
    datos['y_end'] = datos['pass_end_location'].apply(lambda l: l[1] if isinstance(l, list) else None)
    datos = datos.dropna(subset=['x_end', 'y_end'])
    completados = datos[datos['pass_outcome'].isna()]
    fallados = datos[datos['pass_outcome'].notna()]
    pitch.arrows(completados['x'], completados['y'], completados['x_end'], completados['y_end'],
                 ax=ax, color='#1DB954', width=1.5, alpha=0.6)
    pitch.arrows(fallados['x'], fallados['y'], fallados['x_end'], fallados['y_end'],
                 ax=ax, color='#E24B4A', width=1.5, alpha=0.6)
    total = len(datos)
    pct = round(len(completados) / total * 100) if total > 0 else 0
    ax.set_title(f'Pases: {len(completados)}/{total} ({pct}%)', color='white', fontsize=11, fontweight='bold')
    ax.set_facecolor('#1a1a2e')

def mapa_tiros(eventos, jugador, ax):
    datos = eventos[(eventos['player'] == jugador) & (eventos['type'] == 'Shot')].copy()
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#1a1a2e', line_color='white')
    pitch.draw(ax=ax)
    if len(datos) == 0:
        ax.set_title('Sin tiros', color='white', fontsize=11)
        ax.set_facecolor('#1a1a2e')
        return
    datos['x'] = datos['location'].apply(lambda l: l[0])
    datos['y'] = datos['location'].apply(lambda l: l[1])
    datos['xg'] = datos['shot_statsbomb_xg'].fillna(0)
    datos['gol'] = datos['shot_outcome'].apply(lambda x: x == 'Goal' if isinstance(x, str) else False)
    no_gol = datos[~datos['gol']]
    goles = datos[datos['gol']]
    pitch.scatter(no_gol['x'], no_gol['y'], ax=ax, s=no_gol['xg']*800+50, color='#378ADD', alpha=0.7, zorder=3)
    pitch.scatter(goles['x'], goles['y'], ax=ax, s=goles['xg']*800+100, color='#1DB954', alpha=1, zorder=4, marker='*')
    xg_total = round(datos['xg'].sum(), 2)
    ax.set_title(f'Tiros: {len(datos)} | Goles: {datos["gol"].sum()} | xG: {xg_total}', color='white', fontsize=11, fontweight='bold')
    ax.set_facecolor('#1a1a2e')

def stats_resumen(eventos, jugador):
    datos = eventos[eventos['player'] == jugador].copy()
    toques = len(datos[datos['type'] == 'Ball Receipt*'])
    pases = datos[datos['type'] == 'Pass']
    completados = pases[pases['pass_outcome'].isna()]
    pct = round(len(completados) / len(pases) * 100) if len(pases) > 0 else 0
    tiros = datos[datos['type'] == 'Shot']
    goles = tiros[tiros['shot_outcome'] == 'Goal'] if len(tiros) > 0 else pd.DataFrame()
    xg = round(tiros['shot_statsbomb_xg'].sum(), 2) if len(tiros) > 0 else 0
    duelos = datos[datos['type'] == 'Duel']
    presiones = len(datos[datos['type'] == 'Pressure'])
    recuperaciones = len(datos[datos['type'] == 'Ball Recovery'])
    return {
        'Toques': toques,
        'Pases': f"{len(completados)}/{len(pases)} ({pct}%)",
        'Tiros': len(tiros),
        'Goles': len(goles),
        'xG': xg,
        'Duelos': len(duelos),
        'Presiones': presiones,
        'Recuperaciones': recuperaciones,
    }

# Stats resumen arriba
stats = stats_resumen(eventos, jugador_sel)
cols = st.columns(len(stats))
for i, (k, v) in enumerate(stats.items()):
    with cols[i]:
        st.metric(label=k, value=v)

st.markdown("---")

# Visualizaciones
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor('#1a1a2e')
fig.suptitle(f'{jugador_sel}  ·  {equipo_sel}', color='white', fontsize=14, fontweight='bold')

mapa_calor(eventos, jugador_sel, axes[0])
mapa_pases(eventos, jugador_sel, axes[1])
mapa_tiros(eventos, jugador_sel, axes[2])

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#AAAAAA; font-size:12px;'>Datos: StatsBomb Open Data · Desarrollado por Daniel Vasquez · github.com/dagovas27</p>", unsafe_allow_html=True)
