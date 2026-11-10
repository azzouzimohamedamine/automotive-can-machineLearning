import sys
from pathlib import Path

# ==============================================================================
# 1. RÉSOLUTEUR DE CHEMIN RACINE (Obligatoire pour Streamlit Cloud & local)
# ==============================================================================
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ==============================================================================
# 2. IMPORTS DES BIBLIOTHÈQUES & MODULES PROJET
# ==============================================================================
import time
import pandas as pd
import streamlit as st

# Imports de vos modules internes
from simulation.can_generator import CANSimulator

# ==============================================================================
# 3. CONFIGURATION DE LA PAGE STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Automotive CAN Diagnostic Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# 4. EN-TÊTE DU TABLEAU DE BORD
# ==============================================================================
st.title("🚗 Automotive CAN Bus Diagnostic & Anomaly Detection")
st.markdown(
    """
    Ce tableau de bord permet de surveiller les flux de données **CAN bus** en temps réel 
    et de détecter d'éventuelles anomalies ou attaques réseau via des modèles d'apprentissage automatique.
    """
)

# ==============================================================================
# 5. BARRE LATÉRALE (SIDEBAR) - COMMANDES ET CONFIGURATION
# ==============================================================================
st.sidebar.header("⚙️ Configuration de la Simulation")

# Initialisation du simulateur
if "simulator" not in st.session_state:
    st.session_state.simulator = CANSimulator()

bus_speed = st.sidebar.slider("Fréquence d'émission (messages/sec)", 1, 50, 10)
inject_anomaly = st.sidebar.checkbox("Injecter une anomalie simulée", value=False)

st.sidebar.markdown("---")
run_simulation = st.sidebar.button("▶️ Démarrer la surveillance", type="primary")

# ==============================================================================
# 6. CORPS PRINCIPAL DU DASHBOARD
# ==============================================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Statut du réseau CAN", value="Actif 🟢")

with col2:
    st.metric(label="Débit des données", value=f"{bus_speed} msg/s")

with col3:
    st.metric(
        label="Niveau de risque",
        value="Critique 🔴" if inject_anomaly else "Normal 🔵",
    )

st.markdown("---")

# Zone d'affichage des trames CAN et des graphiques
st.subheader("📊 Flux de Trame CAN en Temps Réel")
chart_placeholder = st.empty()
table_placeholder = st.empty()

# Logique d'exécution de la simulation
if run_simulation:
    st.info("Surveillance du bus CAN en cours...")
    
    # Génération / Récupération d'un jeu de données de démonstration
    df_data = st.session_state.simulator.generate_telemetry(
        num_samples=100, anomaly=inject_anomaly
    ) if hasattr(st.session_state.simulator, "generate_telemetry") else pd.DataFrame({
        "Timestamp": [time.time() + i for i in range(20)],
        "CAN_ID": ["0x184", "0x0C8", "0x280", "0x316", "0x184"] * 4,
        "DLC": [8] * 20,
        "Data": ["00 11 22 33 44 55 66 77"] * 20,
        "Anomaly_Score": [0.95 if inject_anomaly else 0.02] * 20
    })

    # Visualisation des graphiques et données
    chart_placeholder.line_chart(df_data[["Anomaly_Score"]])
    table_placeholder.dataframe(df_data.tail(10), use_container_width=True)
else:
    st.write("Cliquez sur **Démarrer la surveillance** dans le menu latéral pour lancer le flux de données.")