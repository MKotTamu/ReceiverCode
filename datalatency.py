import pymongo
import matplotlib.pyplot as plt
import time

# Setup MongoDB client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['realtime_collar']
image_collection = db['newcamera_images']
gps_collection = db['gps_data']
mqtt_collection = db['mqtt_messages']


def measure_query_latency(collection, num_trials):
    latencies = []

    for _ in range(num_trials):
        start_time = time.time()
        # Perform a find operation that retrieves all documents
        documents = list(collection.find({}))
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert latency to milliseconds
        latencies.append(latency)

    return latencies


def plot_latencies(image_latencies, gps_latencies, mqtt_latencies):
    plt.figure(figsize=(15, 10))

    # Subplot for image latencies
    plt.subplot(3, 1, 1)
    plt.plot(image_latencies, marker='o', linestyle='-')
    plt.title("Image Collection Retrieval Latencies")
    plt.ylabel("Latency (ms)")

    # Subplot for GPS latencies
    plt.subplot(3, 1, 2)
    plt.plot(gps_latencies, marker='o', linestyle='-')
    plt.title("GPS Data Collection Retrieval Latencies")
    plt.ylabel("Latency (ms)")

    # Subplot for MQTT latencies
    plt.subplot(3, 1, 3)
    plt.plot(mqtt_latencies, marker='o', linestyle='-')
    plt.title("MQTT Messages Collection Retrieval Latencies")
    plt.xlabel("Trial Number")
    plt.ylabel("Latency (ms)")

    plt.tight_layout()
    plt.show()


def main():
    num_trials = 20
    print("Measuring latency for each collection with 20 trials each:")

    # Measure latencies
    image_latencies = measure_query_latency(image_collection, num_trials)
    gps_latencies = measure_query_latency(gps_collection, num_trials)
    mqtt_latencies = measure_query_latency(mqtt_collection, num_trials)

    # Plot all latencies in one figure
    plot_latencies(image_latencies, gps_latencies, mqtt_latencies)


if __name__ == "__main__":
    main()
