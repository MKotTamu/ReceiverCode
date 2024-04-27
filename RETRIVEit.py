import cv2
import pymongo
import numpy as np

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
        if cv2.waitKey(1000) & 0xFF == ord('q'):  # Display each image for 1000 milliseconds (1 second)
            break

    cv2.destroyAllWindows()


def display_gps_coordinates():
    # Retrieve all GPS documents
    gps_documents = gps_collection.find({})

    for gps_document in gps_documents:
        timestamp = gps_document['timestamp']
        latitude = gps_document['latitude']
        longitude = gps_document['longitude']
        print(f"Timestamp: {timestamp}, Latitude: {latitude}, Longitude: {longitude}")

def display_mqtt_messages():
    # Retrieve all MQTT messages
    mqtt_messages = mqtt_collection.find({})

    for message in mqtt_messages:
        topic = message['topic']
        msg = message['message']
        print(f"Topic: {topic}, Message: {msg}")

# Update the user prompt
user_choice = input("Do you want to display (1) Images, (2) GPS Coordinates, or (3) MQTT Messages? Enter 1, 2, or 3: ").strip()

if user_choice == '1':
    display_images()
elif user_choice == '2':
    display_gps_coordinates()
elif user_choice == '3':
    display_mqtt_messages()
else:
    print("Invalid input. Please enter 1, 2, or 3.")
