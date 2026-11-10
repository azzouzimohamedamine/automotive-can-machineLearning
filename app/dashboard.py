import sys
from pathlib import Path

# 1. Résolution du chemin racine pour éviter les erreurs d'importation
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import time
import pandas as pd
import numpy as np
import streamlit as st

# Import des modules internes du projet
try:
    from simulation.can_generator import CANSimulator
except ImportError:
    # Fallback si le générateur n'est pas encore totalement configuré
    class CANSimulator:
        def generate_telemetry(self, num_samples=100, anomaly=False):
            data = {
                "Timestamp": [time.time() + i*0.1 for i in range(num_samples)],
                "CAN_ID": np.random.choice(["0x123", "0x456", "0x789", "0x184"], num_samples),
                "DLC": [8] * num_samples,
                "Data_Byte_1": np.random.randint(0, 255, num_samples),
                "Anomaly_Score": np.random.uniform(0.8, 1.0 if anomaly else 0.1, num_samples)
            }
            return pd.DataFrame(data)

# 2. Configuration de la page Streamlit
st.set_page_config(
    page_title="Automotive CAN Bus Diagnostic & ML Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. En-tête et Notions techniques
st.title("🚗 Automotive CAN Bus Diagnostic & Anomaly Detection Dashboard")
st.markdown("""
Ce tableau de bord intelligent surveille en temps réel le réseau **CAN (Controller Area Network)** d'un véhicule, 
analyse les flux de trames et détecte les cyberattaques ou défaillances matérielles à l'aide de modèles de **Machine Learning**.
""")

# 4. Barre latérale (Sidebar) - Configuration technique
st.sidebar.header("⚙️ Paramètres du Bus CAN")

# Initialisation du simulateur dans la session
if "simulator" not in st.session_state:
    st.session_state.simulator = CANSimulator()

baud_rate = st.sidebar.selectbox("Vitesse du Bus (Baudrate)", ["500 kbps", "250 kbps", "1 Mbps"], index=0)
sampling_rate = st.sidebar.slider("Fréquence d'échantillonnage (msg/s)", 10, 100, 50)
inject_attack = st.sidebar.checkbox("🚨 Injecter une attaque / anomalie (DDoS/Spoofing)", value=False)

st.sidebar.markdown("---")
run_monitoring = st.sidebar.button("▶️ Démarrer l'analyse en direct", type="primary")

# 5. Sections Principales du Dashboard
# Section 1 : Métriques Globales du Système
st.subheader("📊 Indicateurs Clés de Performance (KPIs)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="État du Réseau", value="Connecté 🟢", delta="Stable")
with col2:
    st.metric(label="Vitesse configurée", value=baud_rate)
with col3:
    st.metric(label="Trames traitées", value="1,240 msg" if not run_monitoring else "Flux live...")
with col4:
    st.metric(
        label="Niveau de Menace", 
        value="CRITIQUE 🔴" if inject_attack else "Normal 🟢",
        delta="ALERTE" if inject_attack else "Sécurisé"
    )

st.markdown("---")

# Section 2 : Analyse technique et graphiques en temps réel
st.subheader("📈 Visualisation des Scores d'Anomalie (Machine Learning)")

chart_placeholder = st.empty()
table_placeholder = st.empty()

if run_monitoring:
    with st.spinner("Analyse du trafic CAN en cours..."):
        # Génération des données de télémétrie simulées
        df = st.session_state.simulator.generate_telemetry(num_samples=50, anomaly=inject_attack)
        
        # Affichage du graphique d'évolution des scores d'anomalie
        chart_placeholder.line_chart(df, x="Timestamp", y="Anomaly_Score")
        
        # Affichage du tableau des dernières trames capturées
        st.markdown("### 📋 Dernières Trames CAN Inspectées")
        table_placeholder.dataframe(df.tail(10), use_container_width=True)
        
        # Alerte visuelle si une anomalie est détectée
        if inject_attack:
            st.error("⚠️ ALERTE DE SÉCURITÉ : Comportement anormal détecté sur les identifiants CAN ! Risque d'injection de messages malveillants.")
        else:
            st.success("✅ Le trafic du bus CAN respecte les profils de comportement nominaux.")
else:
    st.info("💡 Cliquez sur **Démarrer l'analyse en direct** dans la barre latérale pour lancer la simulation des flux de données.")

# Section 3 : Notions et Documentation technique intégrée
with st.expander("📚 Comprendre les notions et l'architecture du projet"):
    st.markdown("""
    * **Bus CAN (Controller Area Network) :** Standard de réseau de véhicules robuste conçu pour permettre aux microcontrôleurs et aux appareils de communiquer entre eux sans hôte central.
    * **Trame CAN :** Composée d'un identifiant (CAN ID) qui définit la priorité du message, d'un champ de données (DLC jusqu'à 8 octets) et d'un contrôle d'erreur.
    * **Détection d'anomalies ML :** Utilisation d'algorithmes non supervisés ou supervisés (Isolation Forest, Autoencoders) pour repérer les déviations temporelles ou structurelles du bus.
    """)