import random
import time

class NetworkMonitor:
    def __init__(self, latency_limit=200):
        """
        latency_limit: Maximum acceptable latency in ms
        """
        self.latency_limit = latency_limit

    def simulate_latency(self):
        """Simulate network latency (ms)"""
        return random.randint(50, 300)

    def is_ok(self):
        """Return True if simulated latency is within acceptable range"""
        latency = self.simulate_latency()
        print(f"[NetworkMonitor] Current latency: {latency} ms. Limit: {self.latency_limit} ms")
        return latency <= self.latency_limit
