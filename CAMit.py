import cv2
import pymongo
from datetime import datetime
import time

# Setup MongoDB client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['realtime_collar']
collection = db['newcamera_images']

# Initialize webcam
cap = cv2.VideoCapture(0)

try:
    while True:
        # Capture image
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Convert image to bytes
        _, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()

        # Create document with image and timestamp
        document = {
            'timestamp': datetime.now(),
            'image': img_bytes
        }

        # Insert document into MongoDB
        collection.insert_one(document)
        print(f"Image captured and stored at {datetime.now()}")

        # Wait for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    print("Program exited by user")

finally:
    # Release the webcam
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam released")
