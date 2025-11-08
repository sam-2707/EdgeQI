# EdgeQI/App/subscriber.py

import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
TOPIC = "edgeiq/results"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[Subscriber] Connected to broker")
        client.subscribe(TOPIC)
    else:
        print(f"[Subscriber] Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"[Subscriber] Message received: {payload}")
    except json.JSONDecodeError:
        print(f"[Subscriber] Received non-JSON message: {msg.payload.decode()}")


def main():
    # Corrected client initialization
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()