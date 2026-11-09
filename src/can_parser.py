"""
CAN Frame Parser Module
Handles parsing, validation, and hexadecimal extraction of automotive CAN network traffic logs.
"""
import re
from typing import Dict, Any, List, Optional, Union

class CANParser:
    """Production-grade parser for Standard (11-bit) and Extended (29-bit) CAN Frames."""

    def __init__(self):
        self.can_id_pattern = re.compile(r'^[0-9A-Fa-f]{1,8}$')

    def parse_raw_row(
        self,
        timestamp: float,
        can_id: str,
        dlc: int,
        payload: Union[List[str], str],
        label: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Parses raw string representation into structured numeric representation.
        """
        clean_id = str(can_id).strip().replace("0x", "").replace("0X", "").zfill(3).upper()
        if not self.can_id_pattern.match(clean_id):
            raise ValueError(f"Invalid Hex CAN ID: {can_id}")

        dlc = int(dlc)
        if not (0 <= dlc <= 8):
            raise ValueError(f"Invalid Data Length Code (DLC): {dlc}. Must be 0-8.")

        # Parse Data Payload
        if isinstance(payload, str):
            payload_clean = payload.strip().replace(" ", "")
            byte_strings = [payload_clean[i:i+2] for i in range(0, len(payload_clean), 2)]
        else:
            byte_strings = [str(b).strip() for b in payload]

        if len(byte_strings) < dlc:
            # Pad with 00 if needed
            byte_strings.extend(["00"] * (dlc - len(byte_strings)))
        elif len(byte_strings) > dlc:
            byte_strings = byte_strings[:dlc]

        parsed_data = [int(b, 16) for b in byte_strings]
        # Always pad to 8 bytes internally for uniform machine learning input shapes
        full_data_8b = parsed_data + [0] * (8 - len(parsed_data))

        return {
            "timestamp": float(timestamp),
            "can_id_hex": clean_id,
            "can_id_int": int(clean_id, 16),
            "dlc": dlc,
            "data_bytes": full_data_8b,
            "data_0": full_data_8b[0],
            "data_1": full_data_8b[1],
            "data_2": full_data_8b[2],
            "data_3": full_data_8b[3],
            "data_4": full_data_8b[4],
            "data_5": full_data_8b[5],
            "data_6": full_data_8b[6],
            "data_7": full_data_8b[7],
            "label": str(label) if label is not None else "Normal"
        }
