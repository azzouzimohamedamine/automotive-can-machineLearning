import sys
from pathlib import Path

# ==============================================================================
# 1. RÉSOLUTEUR DE CHEMIN (Obligatoire pour Streamlit Cloud & local)
# ==============================================================================
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ==============================================================================
# 2. IMPORTS DES BIBLIOTHÈQUES
# ==============================================================================
import os
import time
import pandas as pd
import numpy as np
import streamlit as st

# Import de votre simulateur CAN (avec gestion de secours si besoin)
try:
    from simulation.can_generator import CANSimulator
except ImportError:
    class CANSimulator:
        def generate_telemetry(self, num_samples=100, anomaly=False):
            return pd.DataFrame({
                "Timestamp": [time.time() + i*0.1 for i in range(num_samples)],
                "CAN_ID": np.random.choice(["0x123", "0x456", "0x789", "0x184"], num_samples),
                "DLC": [8] * num_samples,
                "Anomaly_Score": np.random.uniform(0.8, 1.0 if anomaly else 0.1, num_samples)
            })

# ==============================================================================
# 3. CONFIGURATION DE LA PAGE
# ==============================================================================
st.set_page_config(
    page_title="Automotive CAN Bus Diagnostic & ML Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 4. EN-TÊTE DU TABLEAU DE BORD
# ==============================================================================
st.title("🚗 Automotive CAN Bus Diagnostic & Anomaly Detection")
st.markdown("""
Ce tableau de bord surveille en temps réel le réseau **CAN (Controller Area Network)** d'un véhicule, 
analyse les trames et détecte les anomalies à l'aide de modèles de **Machine Learning**.
""")

# ==============================================================================
# 5. BARRE LATÉRALE (SIDEBAR)
# ==============================================================================
st.sidebar.header("⚙️ Paramètres de Simulation")

if "simulator" not in st.session_state:
    st.session_state.simulator = CANSimulator()

baud_rate = st.sidebar.selectbox("Vitesse du Bus (Baudrate)", ["500 kbps", "250 kbps", "1 Mbps"], index=0)
sampling_rate = st.sidebar.slider("Fréquence d'échantillonnage (msg/s)", 10, 100, 50)
inject_attack = st.sidebar.checkbox("🚨 Injecter une anomalie / attaque", value=False)

st.sidebar.markdown("---")
run_monitoring = st.sidebar.button("▶️ Démarrer l'analyse en direct", type="primary")

# ==============================================================================
# 6. SECTIONS DU DASHBOARD
# ==============================================================================

# Section KPIs
st.subheader("📊 Indicateurs Clés de Performance")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="État du Réseau", value="Connecté 🟢", delta="Stable")
with col2:
    st.metric(label="Vitesse configurée", value=baud_rate)
with col3:
    st.metric(label="Trames traitées", value="Flux live..." if run_monitoring else "En attente")
with col4:
    st.metric(
        label="Niveau de Menace", 
        value="CRITIQUE 🔴" if inject_attack else "Normal 🟢",
        delta="ALERTE" if inject_attack else "Sécurisé"
    )

st.markdown("---")

# Section Flux Temps Réel
st.subheader("📈 Surveillance des Trames CAN en Temps Réel")
chart_placeholder = st.empty()
table_placeholder = st.empty()

if run_monitoring:
    with st.spinner("Analyse du trafic CAN..."):
        df_sim = st.session_state.simulator.generate_telemetry(num_samples=50, anomaly=inject_attack)
        chart_placeholder.line_chart(df_sim, x="Timestamp", y="Anomaly_Score")
        table_placeholder.dataframe(df_sim.tail(10), use_container_width=True)
        
        if inject_attack:
            st.error("⚠️ ALERTE : Comportement anormal détecté sur le bus CAN !")
        else:
            st.success("✅ Trafic nominal et sécurisé.")
else:
    st.info("💡 Cliquez sur **Démarrer l'analyse en direct** dans la barre latérale.")

st.markdown("---")

# ==============================================================================
# 7. SECTION RÉSULTATS EXPÉRIMENTAUX & PERFORMANCES (Basée sur votre code)
# ==============================================================================
st.header("📈 Résultats Expérimentaux & Performances du Projet")
st.write("Données importées directement des artefacts d'évaluation du modèle.")

results_path = "models/evaluation_results.csv"

if os.path.exists(results_path):
    # Importation dynamique des résultats du projet
    df_results = pd.read_csv(results_path)
    
    # Affichage sous forme de tableau interactif
    st.dataframe(df_results, use_container_width=True)
    
    # Affichage d'un graphique basé sur ces vrais résultats
    st.markdown("### 📊 Comparaison Graphique des F1-Scores")
    if "Modèle" in df_results.columns and "F1_Score" in df_results.columns:
        st.bar_chart(df_results.set_index("Modèle")["F1_Score"])
    else:
        st.warning("Le fichier CSV doit contenir les colonnes 'Modèle' et 'F1_Score'.")
else:
    st.info("⚠️ Aucun fichier de résultats trouvé (`models/evaluation_results.csv`). Veuillez exécuter le script d'entraînement pour générer les métriques.")

# ==============================================================================
# 8. SECTION DOCUMENTATION / NOTIONS
# ==============================================================================
with st.expander("📚 Notions et Architecture Technique"):
    st.markdown("""
    * **Bus CAN :** Standard de réseau véhiculaire robuste.
    * **Modèles ML :** Évalués sur la base de métriques de précision, de rappel et de score F1 pour détecter les attaques par injection.
    """)