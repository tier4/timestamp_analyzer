import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def analyze_file(timestamps, file_path):
    # Calculate differences
    differences = np.diff(timestamps)
    differences_ms = differences / 1e6  # Convert to milliseconds

    # Calculate statistics
    mean_diff = np.mean(differences_ms)
    std_diff = np.std(differences_ms)
    max_diff = np.max(differences_ms)
    min_diff = np.min(differences_ms)

    # Display statistics
    print(f"Statistics for {file_path}")
    print(f"Average: {mean_diff} ms")
    print(f"Std: {std_diff} ms")
    print(f"Max: {max_diff} ms")
    print(f"Min: {min_diff} ms")

    return differences_ms


def get_timestamps(file_path):
    # Read the file content
    with open(file_path, "r") as file:
        data = file.read()

    # Parse data
    lines = data.strip().split("\n")
    timestamps = []

    for i in range(0, len(lines), 5):
        sec = int(lines[i + 1].split(": ")[1])
        nanosec = int(lines[i + 2].split(": ")[1])
        timestamp = sec * 1e9 + nanosec  # Convert to nanoseconds
        timestamps.append(timestamp)

    return np.array(timestamps)


def analyze_and_match_files(file1, file2):
    # Read seconds and nanoseconds from both files
    file1_timestamps = get_timestamps(file1)
    file2_timestamps = get_timestamps(file2)

    # Analyze the first file and plot differences
    file1_timestamp_differences = analyze_file(file1_timestamps, file1)
    # Analyze the second file and plot differences
    file2_timestamp_differences = analyze_file(file2_timestamps, file2)

    # Create a difference matrix
    diff_matrix = np.abs(file1_timestamps[:, None] - file2_timestamps)

    # Find the best matches based on the smallest difference
    matched_indices = np.argmin(diff_matrix, axis=1)
    matched_diffs = (
        diff_matrix[np.arange(len(file1_timestamps)), matched_indices] / 1e6
    )  # Convert to milliseconds

    # Display matched results and statistics
    print(f"Time difference between {file1} and {file2}")
    print(f"Average time difference: {np.mean(matched_diffs)} ms")
    print(f"Std time difference: {np.std(matched_diffs)} ms")
    print(f"Max time difference: {np.max(matched_diffs)} ms")
    print(f"Min time difference: {np.min(matched_diffs)} ms")

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 18))
    fig.canvas.manager.set_window_title("Timestamp Analyzer")

    # Plot differences for the first file
    axs[0].plot(
        range(1, len(file1_timestamp_differences) + 1),
        file1_timestamp_differences,
        marker="o",
        linestyle="-",
    )
    axs[0].set_title(f"Time Differences Between Consecutive Timestamps for {file1}")
    axs[0].set_xlabel("Packet Index")
    axs[0].set_ylabel("Difference (ms)")
    axs[0].grid(True)

    # Plot differences for the second file
    axs[1].plot(
        range(1, len(file2_timestamp_differences) + 1),
        file2_timestamp_differences,
        marker="o",
        linestyle="-",
    )
    axs[1].set_title(f"Time Differences Between Consecutive Timestamps for {file2}")
    axs[1].set_xlabel("Packet Index")
    axs[1].set_ylabel("Difference (ms)")
    axs[1].grid(True)

    # Plot differences between matched points
    axs[2].plot(
        range(1, len(matched_diffs) + 1), matched_diffs, marker="o", linestyle="-"
    )
    axs[2].set_title("Differences Between Matched Timestamps")
    axs[2].set_xlabel("Matched Point Index")
    axs[2].set_ylabel("Difference (ms)")
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze timestamp data from two files."
    )
    parser.add_argument("file1", type=str, help="Path to the first file")
    parser.add_argument("file2", type=str, help="Path to the second file")

    args = parser.parse_args()

    analyze_and_match_files(args.file1, args.file2)
