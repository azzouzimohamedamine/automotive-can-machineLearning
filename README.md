# Machine Learning-Based Intelligent Fault Detection & Diagnostic Framework for Automotive CAN Networks

A research-grade 4th-year engineering project for automotive CAN bus anomaly detection, signal parsing, machine learning classification, explainability, and real-time interactive simulation using both synthetic validation logic and real-world benchmark datasets (HCRL Car Hacking Dataset).

---

## 🛠️ Project Architecture & Structure
```text
automotive-can-ml-diagnostic/
│
├── README.md                   # Complete setup, execution, and research guide
├── requirements.txt            # Python dependencies
├── .gitignore                  # Exclusion patterns for model weights and raw datasets
│
├── data/                       # Dataset directories
│   ├── raw/                    # Place HCRL CSV files here (normal.csv, DoS_dataset.csv, etc.)
│   └── processed/              # Formatted & engineered dataset outputs
│
├── notebooks/                  # Iterative exploration notebooks
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_can_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_baseline_models.ipynb
│   ├── 05_model_comparison.ipynb
│   └── 06_final_evaluation.ipynb
│
├── src/                        # Production-grade Python source modules
│   ├── __init__.py
│   ├── can_parser.py           # Standard (11-bit) & Extended (29-bit) CAN frame parser
│   ├── preprocessing.py        # Data cleaning, HCRL format adapter, and label encoding
│   ├── feature_engineering.py  # Temporal inter-arrival time, rolling frequencies, payload entropy
│   ├── train.py                # Model training (Decision Tree, Random Forest, XGBoost)
│   ├── evaluate.py             # Performance evaluation & metric reporting
│   ├── inference.py            # Diagnostic engine for real-time inference
│   └── utils.py                # Logging & helper utilities
│
├── simulation/                 # Virtual CAN bus simulation package
│   ├── __init__.py
│   ├── can_generator.py        # ECU frame simulator (Engine, ABS, Body, Battery)
│   └── scenarios.py            # Scenarios: Normal, Abnormal RPM, Temp, DoS Injection
│
├── models/                     # Serialized model weights & feature maps (.joblib)
│
├── app/                        # Interactive Streamlit dashboard
│   └── dashboard.py            # Multi-page web dashboard for real-time diagnostic telemetry
│
├── tests/                      # Automated Pytest unit testing suite
│   ├── test_parser.py          # Frame parsing unit tests
│   ├── test_features.py        # Feature extraction unit tests
│   └── test_preprocessing.py   # Preprocessing & cleaning tests
│
├── docs/                       # Architecture & methodology documentation
│   ├── architecture/
│   ├── methodology/
│   └── results/
│
└── report/                     # LaTeX scientific report source files
    └── report.tex
```

---

## 📊 Dataset Integration: HCRL Car Hacking Benchmark

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

## 🚀 Quickstart Guide (PowerShell Commands)

### 1. Virtual Environment Setup
```powershell
# Create environment
python -m venv .venv

# Activate environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip & install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Execution Commands
```powershell
# A. Run Unit Tests
pytest -v

# B. Run Virtual CAN Simulation
python -m simulation.scenarios

# C. Train & Evaluate Machine Learning Models
python -m src.train

# D. Launch Interactive Streamlit Dashboard
streamlit run app/dashboard.py
```

---

## 📌 Recommended Git Commit Strategy

```powershell
git add .gitignore README.md requirements.txt
git commit -m "chore: update documentation and project configuration for HCRL dataset integration"

git add src/ simulation/ app/ tests/
git commit -m "feat: enhance modular CAN diagnostic engine, simulator, and Streamlit dashboard"

git add report/ notebooks/ docs/
git commit -m "docs: updated LaTeX scientific report and research documentation"
```
