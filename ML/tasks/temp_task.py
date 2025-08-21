# EdgeQI/ML/tasks/temp_task.py

import random
from .base_task import Task

class TempSensorTask(Task):
    def __init__(self):
        super().__init__("TempSensorTask")

    def run(self):
        temperature = round(random.uniform(20.0, 35.0), 2)  # Simulated Celsius
        print(f"[TempSensorTask] Temperature reading: {temperature} °C")
        return {"temperature": temperature}