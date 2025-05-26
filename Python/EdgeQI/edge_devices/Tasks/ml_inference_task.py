import random
from .task_base import Task

class MLInferenceTask(Task):
    def __init__(self):
        super().__init__("MLInferenceTask")

    def run(self):
        # Simulate inference output
        classes = ["normal", "anomaly", "unknown"]
        prediction = random.choice(classes)
        confidence = round(random.uniform(0.6, 0.99), 2)
        print(f"[MLInferenceTask] Predicted: {prediction}, Confidence: {confidence}")
        return {
            "prediction": prediction,
            "confidence": confidence
        }
