"""
Unit Tests for Feature Extraction Pipeline
"""
import pytest
import pandas as pd
from src.feature_engineering import CANFeatureExtractor

def test_payload_entropy():
    fe = CANFeatureExtractor()
    # Uniform bytes should have non-zero entropy
    entropy_val = fe.compute_payload_entropy([10, 20, 30, 40, 50, 60, 70, 80])
    assert entropy_val > 0.0

    # All zeros payload entropy
    zero_entropy = fe.compute_payload_entropy([0, 0, 0, 0, 0, 0, 0, 0])
    assert zero_entropy == 0.0
