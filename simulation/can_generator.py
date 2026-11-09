"""
Python-CAN Virtual Traffic Simulator
Simulates multi-ECU automotive bus communication (Engine, ABS, Body, Battery).
"""
import time
import random
from typing import Dict, Any

class CANSimulator:
    """Virtual ECU Traffic Generator for Real-Time Testing."""

    def __init__(self):
        self.ecu_ids = {
            "ECU_ENGINE_RPM": "100",
            "ECU_SPEED": "101",
            "ECU_TEMP": "102",
            "ECU_ABS": "200",
            "ECU_BATTERY": "300"
        }

    def generate_frame(self, scenario: str = "Normal") -> Dict[str, Any]:
        """Generates CAN frame payload according to active scenario state."""
        timestamp = time.time()
        
        if scenario == "Normal":
            can_id = random.choice(list(self.ecu_ids.values()))
            if can_id == "100": # RPM
                rpm = random.randint(800, 3200)
                data = [(rpm >> 8) & 0xFF, rpm & 0xFF, 0, 0, 0, 0, 0, 0]
            elif can_id == "102": # Temp
                temp = random.randint(85, 95)
                data = [temp, 0, 0, 0, 0, 0, 0, 0]
            else:
                data = [random.randint(0, 255) for _ in range(8)]
            label = "Normal"

        elif scenario == "Abnormal_RPM":
            can_id = "100"
            # Spike RPM to dangerous redline 8500 RPM instantly
            rpm = random.randint(8000, 9500)
            data = [(rpm >> 8) & 0xFF, rpm & 0xFF, 0xFF, 0xFF, 0, 0, 0, 0]
            label = "Abnormal_RPM"

        elif scenario == "Temperature_Anomaly":
            can_id = "102"
            # Overheating Engine condition (140 C)
            data = [140, 255, 0, 0, 0, 0, 0, 0]
            label = "Temperature_Anomaly"

        elif scenario == "DoS_Injection":
            # High frequency flooding zero ID
            can_id = "000"
            data = [0, 0, 0, 0, 0, 0, 0, 0]
            label = "DoS_Injection"

        else:
            can_id = "101"
            data = [0] * 8
            label = "Normal"

        return {
            "timestamp": timestamp,
            "can_id": can_id,
            "dlc": 8,
            "data": data,
            "data_0": data[0], "data_1": data[1], "data_2": data[2], "data_3": data[3],
            "data_4": data[4], "data_5": data[5], "data_6": data[6], "data_7": data[7],
            "label": label
        }
