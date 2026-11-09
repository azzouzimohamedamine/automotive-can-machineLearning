"""
Model Evaluation and Confusion Matrix Generation
"""
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from src.utils import setup_logger

logger = setup_logger("Evaluation")

def evaluate_saved_model():
    """Loads saved serialized model and prints diagnostic metrics."""
    try:
        model = joblib.load("models/best_diagnostic_model.joblib")
        label_map = joblib.load("models/label_map.joblib")
        logger.info("Successfully loaded model and metadata artifacts.")
        print("
--- Diagnostic Classification Summary ---")
        print("Mapped Target Classes:", label_map)
    except Exception as e:
        logger.error(f"Error loading model artifacts: {e}")

if __name__ == "__main__":
    evaluate_saved_model()
