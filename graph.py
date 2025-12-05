#!/usr/bin/env python

# graph.py
import sys
import csv
import os
import glob
import matplotlib.pyplot as plt

TRAJ_DIR = "trajectories"

def find_latest_file():
    files = glob.glob(os.path.join(TRAJ_DIR, "*.csv"))
    if not files:
        print("No trajectory files found in 'trajectories/'.")
        sys.exit(1)
    return max(files, key=os.path.getmtime)


def resolve_filename(user_input):
    """
    Accepts:
      - plain filename
      - filename without path
      - full path
    Returns full path inside trajectories/
    """

    # If already a path inside trajectories
    if os.path.isfile(user_input):
        return user_input

    # Try inside the trajectories folder
    candidate = os.path.join(TRAJ_DIR, user_input)
    if os.path.isfile(candidate):
        return candidate

    print(f"File '{user_input}' not found in '{TRAJ_DIR}'.")
    sys.exit(1)


def read_csv(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # First two lines have angle + speed
    angle_line = rows[1]
    launch_angle_deg = float(angle_line[0])
    launch_speed = float(angle_line[1])

    # Find start of data
    for i, line in enumerate(rows):
        if len(line) > 0 and line[0] == "t (s)":
            data_start_index = i + 1
            break

    t, x, y = [], [], []
    for line in rows[data_start_index:]:
        if len(line) < 3:
            continue
        t.append(float(line[0]))
        x.append(float(line[1]))
        y.append(float(line[2]))

    return launch_angle_deg, launch_speed, t, x, y


def main():
    # No filename provided → use most recent CSV
    if len(sys.argv) == 1:
        filename = find_latest_file()
        print(f"Using newest trajectory file: {filename}")

    # One argument → try to resolve it
    elif len(sys.argv) == 2:
        filename = resolve_filename(sys.argv[1])
        print(f"Loading trajectory: {filename}")

    else:
        print("Usage: python graph.py [csv_file]")
        sys.exit(1)

    # Parse CSV
    angle_deg, speed, t, x, y = read_csv(filename)

    # Plot trajectory
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linewidth=2)

    # Labels
    plt.xlabel("Horizontal Position (m)")
    plt.ylabel("Vertical Position (m)")
    plt.title("Projectile Trajectory")

    # Add info box
    info_text = f"Launch Speed: {speed:.2f} m/s\nLaunch Angle: {angle_deg:.2f}°"
    plt.text(0.02, 0.95,
             info_text,
             transform=plt.gca().transAxes,
             fontsize=12,
             verticalalignment='top',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
