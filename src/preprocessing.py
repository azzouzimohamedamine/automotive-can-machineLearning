"""
CAN Preprocessing Module
Handles cleaning, column standardization, missing values removal, 
and label encoding for automotive CAN bus datasets.
"""
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from src.utils import setup_logger

logger = setup_logger("Preprocessor")

class CANPreprocessor:
    def __init__(self):
        self.label_encoder = LabelEncoder()

    def clean_raw_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans raw CAN dataframe by standardizing column names, 
        mapping alternate header conventions, and dropping invalid rows.
        """
        # 1. Normaliser les noms de colonnes (minuscules, pas d'espaces, tirets bas)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
        
        # 2. Mapper les en-têtes alternatifs fréquents (ex: HCRL ou autres datasets)
        rename_mapping = {
            "id": "can_id",
            "arbitration_id": "can_id",
            "time": "timestamp",
            "class": "label",
            "attack": "label"
        }
        df = df.rename(columns=rename_mapping)

        # 3. S'assurer que les colonnes indispensables existent ou les initialiser par défaut
        if "timestamp" not in df.columns:
            df["timestamp"] = range(len(df))
        if "can_id" not in df.columns:
            df["can_id"] = "000"
        if "dlc" not in df.columns:
            df["dlc"] = 8

        # 4. Nettoyage des lignes avec des valeurs nulles sur les champs critiques
        df = df.dropna(subset=["timestamp", "can_id", "dlc"]).copy()
        
        logger.info(f"DataFrame cleaned successfully. Final shape: {df.shape}")
        return df

    def fit_encode_labels(self, labels: pd.Series):
        """Encodes string classification labels into numeric integers."""
        encoded_labels = self.label_encoder.fit_transform(labels)
        label_mapping = {index: label for index, label in enumerate(self.label_encoder.classes_)}
        logger.info(f"Labels encoded successfully: {label_mapping}")
        return encoded_labels, label_mapping