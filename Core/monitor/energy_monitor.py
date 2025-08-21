# EdgeQI/Core/monitor/energy_monitor.py

import random
import time

class EnergyMonitor:
    def __init__(self, threshold=30):
        """
        threshold: Minimum battery % to allow task execution
        """
        self.threshold = threshold
        self.energy_level = 100  # Start with full battery

    def simulate_drain(self):
        """Simulate battery drain over time"""
        self.energy_level = max(0, self.energy_level - random.uniform(0.5, 2.0))

    def get_energy_level(self):
        """Return current energy level"""
        self.simulate_drain()
        return round(self.energy_level, 2)

    def is_ok(self):
        """Return True if energy level is above threshold"""
        level = self.get_energy_level()
        print(f"[EnergyMonitor] Battery at {level}%. Threshold: {self.threshold}%")
        return level > self.threshold