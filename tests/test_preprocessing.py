"""
Unit Tests for Preprocessing Data Cleaner
"""
import pytest
import pandas as pd
from src.preprocessing import CANPreprocessor

def test_preprocessing_cleanup():
    prep = CANPreprocessor()
    df_raw = pd.DataFrame({
        "timestamp": [1.0, 1.1, None],
        "can_id": ["100", "101", "102"],
        "dlc": [8, 8, 8],
        "label": ["Normal", "Normal", "Normal"]
    })
    df_cleaned = prep.clean_raw_dataframe(df_raw)
    assert len(df_cleaned) == 2
