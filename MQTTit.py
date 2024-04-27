import paho.mqtt.client as mqtt
import pymongo
from datetime import datetime

# MongoDB setup
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo_client['realtime_collar']
mqtt_collection = db['mqtt_messages']

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("collar")  # Subscribe to the topic

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic} with payload {msg.payload}")
    # Convert message payload to string and store in MongoDB
    message_data = {
        "topic": msg.topic,
        "message": msg.payload.decode(),  # Decoding from bytes to string
        "timestamp": datetime.now()
    }
    mqtt_collection.insert_one(message_data)

# Setup MQTT client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker (adjust as necessary)
mqtt_client.connect("localhost", 1883, 60)  # Assuming the broker is running on localhost

# Start the loop
mqtt_client.loop_start()

try:
    # Run indefinitely until manually stopped
    input("Press Enter to stop the client...\n")
finally:
    # Clean up
    mqtt_client.loop_stop()  # Stop the loop
    mqtt_client.disconnect()  # Disconnect from the broker
