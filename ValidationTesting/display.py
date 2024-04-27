import cv2
import pymongo
import numpy as np
import matplotlib.pyplot as plt

# Setup MongoDB client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['realtime_collar']
image_collection = db['newcamera_images']


def display_images_matplotlib():
    # Retrieve all documents from the image collection
    image_documents = image_collection.find({})

    # Convert to list if you want to know the number of documents or slice
    images = list(image_documents)
    num_images = len(images)
    num_columns = 3
    num_rows = (num_images + num_columns - 1) // num_columns  # Round up to ensure all images fit

    fig, axs = plt.subplots(num_rows, num_columns, figsize=(15, num_rows * 5))
    axs = axs.ravel()  # Flatten the array for easier iteration

    for idx, image_document in enumerate(images):
        img_bytes = image_document['image']
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB for correct color display
        axs[idx].imshow(img)
        axs[idx].axis('off')  # Hide axes

    # Turn off axes for any unused subplots
    for ax in axs[idx + 1:]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


display_images_matplotlib()
