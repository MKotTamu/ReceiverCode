import paho.mqtt.client as mqtt
import pymongo
from datetime import datetime
import matplotlib.pyplot as plt
import time

# MongoDB setup
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo_client['realtime_collar']
mqtt_collection = db['mqtt_messages']
latency_collection = db['mqtt_latencies']  # Collection for storing latencies

# List to store latency values
latencies = []


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("collar")  # Subscribe to the topic


def on_message(client, userdata, msg):
    received_time = datetime.now()
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic} with payload {payload}")

    # Extract sent time from message payload and calculate latency
    sent_time = datetime.fromisoformat(payload.split('|')[1])
    latency = (received_time - sent_time).total_seconds()
    latencies.append(latency)

    # Store latency in MongoDB
    latency_data = {
        "topic": msg.topic,
        "latency": latency,
        "timestamp": received_time
    }
    latency_collection.insert_one(latency_data)


def publish_messages():
    """Function to simulate message sending with timestamp."""
    publisher = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    publisher.connect("localhost", 1883, 60)
    while True:
        time_now = datetime.now()
        payload = f"Hello|{time_now.isoformat()}"
        publisher.publish("collar", payload)
        print(f"Sent message: {payload}")
        time.sleep(5)  # Adjust the frequency of messages as needed


def plot_latencies():
    """Plot the recorded latencies."""
    plt.figure(figsize=(10, 5))
    plt.plot(latencies, marker='o')
    plt.title('MQTT Message Latency Over Time')
    plt.xlabel('Message Index')
    plt.ylabel('Latency (seconds)')
    plt.grid(True)
    plt.show()


# Setup MQTT client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect("localhost", 1883, 60)

# Start the loop
mqtt_client.loop_start()

try:
    # Launch publisher in a separate thread or process
    import threading

    publisher_thread = threading.Thread(target=publish_messages)
    publisher_thread.start()

    # Allow the system to collect data
    input("Press Enter to stop the client and plot results...\n")
finally:
    # Clean up
    mqtt_client.loop_stop()  # Stop the loop
    mqtt_client.disconnect()  # Disconnect from the broker
    plot_latencies()  # Plot the collected latencies
