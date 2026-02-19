import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json

data = []

def on_message(client, userdata, message):
    payload_str = message.payload.decode("utf-8")
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        print("Bad payload:", payload_str)
        return

    timestamp = datetime.now()
    data.append((timestamp, payload.get("temperature"), payload.get("humidity")))
    if len(data) > 100:
        data.pop(0)

    df = pd.DataFrame(data, columns=["timestamp", "temperature", "humidity"])

    plt.clf()
    plt.plot(df["timestamp"], df["temperature"], label="Temperature")
    plt.plot(df["timestamp"], df["humidity"], label="Humidity")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.draw()
    plt.pause(0.1)

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("sensor/data")

plt.ion()
plt.figure()
client.loop_start()

print("Subscribed to sensor/data, plotting in real time...")
plt.show(block=True)
client.loop_stop()
client.disconnect()
