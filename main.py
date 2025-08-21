# EdgeQI/main.py

from Core.scheduler.scheduler import Scheduler
from Core.monitor.energy_monitor import EnergyMonitor
from Core.monitor.network_monitor import NetworkMonitor
from ML.tasks.temp_task import TempSensorTask
from ML.tasks.anomaly_task import MLInferenceTask
from Core.summarizer.summarizer import Summarizer
from Core.communication.mqtt_client import MqttClient

def main():
    # Initialize components
    scheduler = Scheduler()
    energy_monitor = EnergyMonitor(threshold=30)
    net_monitor = NetworkMonitor(latency_limit=200)
    summarizer = Summarizer()
    mqtt_client = MqttClient(broker='localhost', port=1883, topic='edgeiq/results')
    mqtt_client.connect()

    # Create tasks
    temp_task = TempSensorTask()
    ml_task = MLInferenceTask()

    # Wrapper to run task and summarize results before sending
    def wrapped_task(task):
        def inner():
            result = task()
            summary = summarizer.summarize(task.name, result)
            return summary
        return inner

    # Add tasks with priorities (lower number = higher priority)
    scheduler.add_task(wrapped_task(temp_task), priority=2, task_name=temp_task.name)
    scheduler.add_task(wrapped_task(ml_task), priority=5, task_name=ml_task.name)

    try:
        scheduler.run_loop(energy_monitor=energy_monitor, net_monitor=net_monitor, mqtt=mqtt_client)
    except KeyboardInterrupt:
        print("Shutting down scheduler...")
    finally:
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()