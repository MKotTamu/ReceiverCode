import paho.mqtt.client as mqtt
from gpiozero import Buzzer
from time import sleep

# Setup the Buzzer on GPIO pin 23
buzzer = Buzzer(23)

# This function is called when the MQTT client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to the topic
    client.subscribe("rpi/buzzer")

# This function is called when a message is received
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    if message == "on":
        buzzer.on()
        print("Buzzer turned on")
    elif message == "off":
        buzzer.off()
        print("Buzzer turned off")

# Setup MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

# Replace 'localhost' with your MQTT broker's IP address if it's not running on the Raspberry Pi
client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks, and handles reconnecting
client.loop_forever()
