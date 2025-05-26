# mqtt_subscriber.py

import paho.mqtt.client as mqtt

BROKER = "localhost"  # Change if your broker is remote
TOPIC = "edgeiq/results"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[Subscriber] Connected to broker")
        client.subscribe(TOPIC)
    else:
        print(f"[Subscriber] Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"[Subscriber] Message received on topic {msg.topic}: {msg.payload.decode()}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
