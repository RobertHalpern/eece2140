# data_export.py
import csv
from datetime import datetime

def save_trajectory_csv(points, launch_angle_deg, launch_speed):
    """
    points = list of (t, x, y, vx, vy)
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"trajectory_{timestamp}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        # Header: launch conditions
        writer.writerow(["Launch Angle (deg)", "Launch Speed (m/s)"])
        writer.writerow([launch_angle_deg, launch_speed])
        writer.writerow([])

        # Column labels
        writer.writerow(["t (s)", "x (m)", "y (m)", "vx (m/s)", "vy (m/s)"])

        # Trajectory data
        for row in points:
            writer.writerow(row)

    return filename
