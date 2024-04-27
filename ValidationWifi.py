import speedtest
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

# Configuration
test_duration = timedelta(minutes=60)  # Duration to run the test
test_interval = timedelta(minutes=5)  # Interval between each test
output_csv = 'wifi_speed_test_log.csv'


def perform_speed_test():
    """Perform a single speed test and return the results."""
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert from bits/s to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert from bits/s to Mbps
    return download_speed, upload_speed


def log_speed_tests(duration, interval, filename):
    """Perform and log speed tests over a specified duration at given intervals."""
    end_time = datetime.now() + duration
    results = []

    while datetime.now() < end_time:
        download, upload = perform_speed_test()
        results.append({
            'timestamp': datetime.now(),
            'download_mbps': download,
            'upload_mbps': upload
        })
        print(f"Logged at {datetime.now()}: Download = {download} Mbps, Upload = {upload} Mbps")
        time.sleep(interval.total_seconds())

    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    return df


def plot_results(df):
    """Plot the speed test results from a dataframe."""
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['download_mbps'], label='Download Speed (Mbps)', marker='o')
    plt.plot(df['timestamp'], df['upload_mbps'], label='Upload Speed (Mbps)', marker='o')
    plt.title('WiFi Speed Test Results Over Time')
    plt.xlabel('Time')
    plt.ylabel('Speed (Mbps)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('wifi_speed_test_results.png')
    plt.show()


if __name__ == "__main__":
    # Log the speed tests to a CSV file
    df = log_speed_tests(test_duration, test_interval, output_csv)
    # Plot the results
    plot_results(df)
