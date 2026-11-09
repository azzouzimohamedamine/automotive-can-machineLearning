"""
CAN Feature Engineering Module
Extracts temporal deltas, message frequencies, statistical metrics, 
and payload information entropy from CAN frames.
"""
import pandas as pd
import numpy as np
from scipy.stats import entropy
from src.utils import setup_logger

logger = setup_logger("Feature_Engineering")

class CANFeatureExtractor:
    def __init__(self):
        pass

    def _safe_hex_to_int(self, val):
        """Converts hex string (e.g., 'ff', '05') or numeric to integer safely."""
        if pd.isna(val):
            return 0
        if isinstance(val, (int, float)):
            return int(val)
        try:
            return int(str(val).strip(), 16)
        except ValueError:
            try:
                return int(float(str(val).strip()))
            except ValueError:
                return 0

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts temporal features (time_delta, frequency) and statistical payload features.
        """
        df = df.copy()
        
        # 1. S'assurer que les colonnes de payload sont converties en entiers numériques (depuis l'hexadécimal)
        byte_cols = [f"data_{i}" for i in range(8)]
        for col in byte_cols:
            if col in df.columns:
                df[col] = df[col].apply(self._safe_hex_to_int)
            else:
                df[col] = 0

        # 2. Trier par timestamp pour les calculs temporels corrects
        if "timestamp" in df.columns:
            df = df.sort_values(by="timestamp").reset_index(drop=True)
            df["time_delta"] = df["timestamp"].diff().fillna(0.0)
            df["message_frequency"] = 1.0 / (df["time_delta"].clip(lower=1e-6))
        else:
            df["time_delta"] = 0.0
            df["message_frequency"] = 100.0

        # 3. Calculs statistiques sur les octets du payload
        features_df = df.copy()
        numeric_bytes = features_df[byte_cols]
        
        features_df["byte_mean"] = numeric_bytes.mean(axis=1)
        features_df["byte_std"] = numeric_bytes.std(axis=1).fillna(0.0)
        
        # 4. Calcul de l'entropie de Shannon du payload avec typage strict en entiers natifs
        def compute_row_entropy(row):
            values = row[byte_cols].values.astype(int)
            value_counts = np.bincount(values, minlength=256)
            probabilities = value_counts / np.sum(value_counts)
            return entropy(probabilities, base=2)

        logger.info("Computing payload information entropy (vectorized/row-wise)...")
        features_df["payload_entropy"] = features_df.apply(compute_row_entropy, axis=1)

        logger.info("Feature engineering completed successfully.")
        return features_df