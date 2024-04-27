import pymongo
from datetime import datetime
import time
import random

# Setup MongoDB client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['realtime_collar']
gps_collection = db['gps_data']

def generate_random_coordinates():
    """
    Generates a random latitude and longitude.
    Latitude ranges from -90 to 90.
    Longitude ranges from -180 to 180.
    """
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    return latitude, longitude

try:
    while True:
        # Generate random GPS data
        latitude, longitude = generate_random_coordinates()

        # Create document with GPS data and timestamp
        document = {
            'timestamp': datetime.now(),
            'latitude': latitude,
            'longitude': longitude
        }

        # Insert document into MongoDB
        gps_collection.insert_one(document)
        print(f"GPS data captured and stored at {datetime.now()} - Lat: {latitude}, Long: {longitude}")

        # Wait for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    print("GPS data capture stopped by user")
