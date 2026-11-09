"""
Scenario Runner Script for Virtual CAN Validation Pipeline
"""
import time
from simulation.can_generator import CANSimulator

def run_all_scenarios(frames_per_scenario: int = 5):
    sim = CANSimulator()
    scenarios = ["Normal", "Abnormal_RPM", "Temperature_Anomaly", "DoS_Injection"]

    print("=== STARTING VIRTUAL AUTOMOTIVE CAN SIMULATION ===")
    for sc in scenarios:
        print(f"\n--- Running Scenario: {sc} ---")
        for i in range(frames_per_scenario):
            frame = sim.generate_frame(scenario=sc)
            print(f"[{i+1}/{frames_per_scenario}] Timestamp: {frame['timestamp']:.4f} | ID: 0x{frame['can_id']} | Payload: {frame['data']} | Target Label: {frame['label']}")
            time.sleep(0.05)
    print("\n=== SIMULATION SUCCESSFULLY FINISHED ===")

if __name__ == "__main__":
    run_all_scenarios()
