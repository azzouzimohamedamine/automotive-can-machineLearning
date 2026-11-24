# Machine Learning-Based Intelligent Fault Detection & Diagnostic Framework for Automotive CAN Networks

A research-grade 4th-year engineering project for automotive CAN bus anomaly detection, signal parsing, machine learning classification, explainability, and real-time interactive simulation using both synthetic validation logic and real-world benchmark datasets (HCRL Car Hacking Dataset).

---



##  Dataset Integration: HCRL Car Hacking Benchmark

This framework fully supports the **Car Hacking Dataset (HCRL - Korea University)**.

### How to load real data into the pipeline:
1. Download the CSV files from Kaggle or HCRL portal (`normal.csv`, `DoS_dataset.csv`, `Fuzzy_dataset.csv`, `RPM_dataset.csv`, `Gear_dataset.csv`).
2. Move the CSV files into `data/raw/`.
3. Update the dataset loading line in `src/train.py`:
   ```python
   # Load real HCRL benchmark datasets
   df_normal = pd.read_csv("data/raw/normal.csv")
   df_attack = pd.read_csv("data/raw/DoS_dataset.csv")
   df = pd.concat([df_normal, df_attack], ignore_index=True)
   ```
4. Re-run `python -m src.train` to train models on real automotive CAN traffic.

---


# D. Launch Interactive Streamlit Dashboard
streamlit run app/dashboard.py
```

---
# Automotive Cyber-Physical Diagnostic & CAN Bus Intrusion Suite

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://automotive-can-machinelearning-bcjxwfq4kucc5siucjdq2p.streamlit.app/)
