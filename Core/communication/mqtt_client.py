# EdgeQI/Core/communication/mqtt_client.py

import paho.mqtt.client as mqtt
import json
import time

class MqttClient:
    def __init__(self, broker='localhost', port=1883, topic='edgeiq/results'):
        self.broker = broker
        self.port = port
        self.topic = topic
        # Corrected client initialization
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("[MQTT] Connected to broker.")
        else:
            print(f"[MQTT] Connection failed with code {rc}.")

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def send_result(self, task_name, result):
        if result is None:
            return
        message = {
            'task': task_name,
            'result': result,
            'timestamp': time.time()
        }
        payload = json.dumps(message)
        self.client.publish(self.topic, payload)
        print(f"[MQTT] Published result for task '{task_name}'")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()