"""
Real-Time Diagnostic Inference Engine
Loads trained model pipelines to perform online anomaly diagnosis on incoming CAN frames.
"""
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any

class DiagnosticEngine:
    def __init__(self, model_path: str = "models/best_diagnostic_model.joblib"):
        try:
            self.model = joblib.load(model_path)
            self.label_map = joblib.load("models/label_map.joblib")
            self.feature_cols = joblib.load("models/feature_cols.joblib")
            self.is_ready = True
        except Exception:
            self.is_ready = False

    def predict_frame(self, frame_features: Dict[str, Any]) -> Dict[str, Any]:
        """Runs single frame or window vector through ML pipeline."""
        if not self.is_ready:
            return {"status": "Error", "prediction": "Model non initialized", "confidence": 0.0}

        df = pd.DataFrame([frame_features])
        # Ensure all columns exist
        for col in self.feature_cols:
            if col not in df.columns:
                df[col] = 0.0

        X = df[self.feature_cols]
        pred_idx = self.model.predict(X)[0]
        probs = self.model.predict_proba(X)[0]
        
        predicted_label = self.label_map.get(pred_idx, str(pred_idx))
        confidence = float(np.max(probs))

        return {
            "status": "Success",
            "prediction": predicted_label,
            "confidence": confidence,
            "is_anomaly": predicted_label != "Normal"
        }
