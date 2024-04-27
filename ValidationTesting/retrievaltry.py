import tkinter as tk
from pandastable import Table
import cv2
import pymongo
import numpy as np
import pandas as pd

# Setup MongoDB client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['realtime_collar']
image_collection = db['newcamera_images']
gps_collection = db['gps_data']
mqtt_collection = db['mqtt_messages']

def display_images():
    # Retrieve all documents from the image collection
    image_documents = image_collection.find({})

    for image_document in image_documents:
        img_bytes = image_document['image']

        # Convert bytes to numpy array and decode image
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Display image
        cv2.imshow('Image', img)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def display_gps_coordinates():
    # Retrieve all GPS documents
    gps_documents = gps_collection.find({})
    gps_data = [{
        "Timestamp": gps['timestamp'],
        "Latitude": gps['latitude'],
        "Longitude": gps['longitude']
    } for gps in gps_documents]

    df_gps = pd.DataFrame(gps_data)
    create_pandas_table_window(df_gps, "GPS Data")

def display_mqtt_messages():
    # Retrieve all MQTT messages
    mqtt_messages = mqtt_collection.find({})
    mqtt_data = [{
        "Topic": msg['topic'],
        "Message": msg['message']
    } for msg in mqtt_messages]

    df_mqtt = pd.DataFrame(mqtt_data)
    create_pandas_table_window(df_mqtt, "MQTT Messages")

def create_pandas_table_window(dataframe, title):
    root = tk.Tk()
    root.title(title)
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    pt = Table(frame, dataframe=dataframe, showtoolbar=True, showstatusbar=True)
    pt.show()
    root.mainloop()

user_choice = input("Do you want to display (1) Images, (2) GPS Coordinates, or (3) MQTT Messages? Enter 1, 2, or 3: ").strip()

if user_choice == '1':
    display_images()
elif user_choice == '2':
    display_gps_coordinates()
elif user_choice == '3':
    display_mqtt_messages()
else:
    print("Invalid input. Please enter 1, 2, or 3.")
