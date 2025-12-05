# data_export.py
import csv
import os
from datetime import datetime

def save_trajectory_csv(points, launch_angle_deg, launch_speed):

    # Make a folder named "trajectories" if it doesn't exist
    folder = "trajectories"
    os.makedirs(folder, exist_ok=True)

    # Filename inside folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # timestamp = datetime.now().strftime("%d/%m/%Y_%H%M%S")
    filename = os.path.join(folder, f"trajectory_{timestamp}.csv")

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Launch Angle (deg)", "Launch Speed (m/s)"])
        writer.writerow([launch_angle_deg, launch_speed])
        writer.writerow([])

        writer.writerow(["t (s)", "x (m)", "y (m)", "vx (m/s)", "vy (m/s)"])
        for row in points:
            writer.writerow(row)

    return filename
