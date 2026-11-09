"""
Unit Tests for CAN Parser
"""
import pytest
from src.can_parser import CANParser

def test_parser_valid_frame():
    parser = CANParser()
    frame = parser.parse_raw_row(123456.789, "100", 8, ["00", "1A", "FF", "00", "00", "00", "00", "00"], "Normal")
    assert frame["can_id_hex"] == "100"
    assert frame["dlc"] == 8
    assert frame["data_bytes"][1] == 26
    assert frame["label"] == "Normal"

def test_parser_invalid_dlc():
    parser = CANParser()
    with pytest.raises(ValueError):
        parser.parse_raw_row(123456.789, "100", 9, ["00"] * 9)
