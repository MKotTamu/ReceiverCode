import subprocess
import re
import matplotlib.pyplot as plt
import datetime


# Function to get WiFi metrics using iwconfig
def get_wifi_metrics():
    result = subprocess.run(['iwconfig', 'wlan0'], capture_output=True, text=True)
    output = result.stdout
    signal_level = re.search('Signal level=(-?\d+)', output)
    link_quality = re.search('Link Quality=(\d+)/(\d+)', output)

    if signal_level and link_quality:
        level = int(signal_level.group(1))
        quality = int(link_quality.group(1)) / int(link_quality.group(2)) * 100  # Converting to percentage
        return level, quality
    else:
        print("Failed to retrieve data")
        return None, None


# Function to update the plot data
def update_plot_data(signal_strengths, link_qualities):
    level, quality = get_wifi_metrics()
    if level is not None and quality is not None:
        signal_strengths.append(level)
        link_qualities.append(quality)


# Main function to run the monitoring and plotting
def run_monitoring():
    signal_strengths = []
    link_qualities = []
    total_duration = 120  # Duration in seconds
    interval = 1  # Interval in seconds

    # Collect data every second for 120 seconds
    for _ in range(total_duration // interval):
        update_plot_data(signal_strengths, link_qualities)
        time.sleep(interval)

    # Plotting the results
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('WiFi Metrics Monitoring Over 120 Seconds')

    ax1.plot(signal_strengths, label='Signal Strength (dBm)')
    ax2.plot(link_qualities, label='Link Quality (%)')

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Signal Strength (dBm)')
    ax1.legend()

    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Link Quality (%)')
    ax2.legend()

    # Saving the plot
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    plt.savefig(f'wifi_metrics_{timestamp}.png')
    print(f"Saved: wifi_metrics_{timestamp}.png")
    plt.close(fig)


if __name__ == "__main__":
    import time

    run_monitoring()
