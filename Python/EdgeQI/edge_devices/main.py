from Scheduler.scheduler import Scheduler
from Monitor.energy_monitor import EnergyMonitor
from Monitor.net_monitor import NetworkMonitor
from Tasks.temp_sensor_task import TempSensorTask
from Tasks.ml_inference_task import MLInferenceTask
from Summarizer.summarizer import Summarizer
from Communication.mqtt_client import MqttClient

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
