import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random

# Configuration
rtsp_url = "rtsp://192.168.1.7:8000/"  # replace this with your actual RTSP URL
duration = 300  # How long to run the test in seconds
interval = 5  # Interval between measurements in seconds


def extract_metrics_from_ffmpeg(output):
    # Updated regex for frame rate extraction to handle current output format
    fps_pattern = r"fps=(\d+\.\d+)"

    fps = re.findall(fps_pattern, output)
    fps = float(fps[-1]) if fps else 0  # Using the last reported fps value

    return fps


def log_stream_quality(rtsp_url, duration, interval):
    # Prepare to capture the metrics periodically
    results = []
    start_time = datetime.now()
    end_time = start_time + pd.Timedelta(seconds=duration)

    while datetime.now() < end_time:
        command = f"ffmpeg -i {rtsp_url} -t {interval} -vf fps=fps=1 -f null -"
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Print stderr for debugging
        print(process.stderr)

        fps = extract_metrics_from_ffmpeg(process.stderr)
        results.append({"timestamp": datetime.now(), "fps": fps})
        print(f"Logged at {results[-1]['timestamp']}: FPS = {fps}")

    return pd.DataFrame(results)


# Run the logging
data = log_stream_quality(rtsp_url, duration, interval)

# Save to CSV
data.to_csv("stream_quality_log.csv", index=False)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data['timestamp'], data['fps'], marker='o', color='r', linestyle='-')
plt.title("Frame Rate over Time")
plt.xlabel("Time")
plt.ylabel("FPS")

plt.tight_layout()
plt.savefig("stream_quality_chart.png")
plt.show()
