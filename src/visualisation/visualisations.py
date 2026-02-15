# src/visualisation/visualisations.py

import os

import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Extract speed values from formatted steps
# ---------------------------------------------------------
def extract_speed_profile(steps):
    speeds = []
    current_speed = 0

    for step in steps:
        action = step["action"]
        params = step["params"]

        if action == "SET_SPEED":
            current_speed = params.get("value", current_speed)

        speeds.append(current_speed)

    return speeds


# ---------------------------------------------------------
# Extract ACC ON/OFF timeline
# ---------------------------------------------------------
def extract_acc_timeline(steps):
    acc_state = []
    acc_on = False

    for step in steps:
        action = step["action"]

        if action == "ACC_ON":
            acc_on = True
        elif action == "ACC_OFF":
            acc_on = False

        acc_state.append(1 if acc_on else 0)

    return acc_state


# ---------------------------------------------------------
# Extract lane timeline
# ---------------------------------------------------------
def extract_lane_timeline(steps):
    lane = "CENTER"
    lane_map = {"LEFT": 2, "CENTER": 1, "RIGHT": 0}
    timeline = []

    for step in steps:
        action = step["action"]

        if action == "LANE_CHANGE_LEFT":
            lane = "LEFT"
        elif action == "LANE_CHANGE_RIGHT":
            lane = "RIGHT"

        timeline.append(lane_map[lane])

    return timeline


# ---------------------------------------------------------
# Plot 1: Speed Profile
# ---------------------------------------------------------
def plot_speed_profile(steps, out_dir):
    speeds = extract_speed_profile(steps)

    plt.figure(figsize=(10, 4))
    plt.plot(speeds, marker="o", color="#1f77b4", linewidth=2)
    plt.title("Speed Profile Over Steps")
    plt.xlabel("Step Index")
    plt.ylabel("Speed (km/h)")
    plt.grid(True)
    plt.legend(["Speed"], loc="upper left")

    path = os.path.join(out_dir, "speed_profile.png")
    plt.savefig(path)
    plt.close()
    print(f"[OK] Saved speed profile → {path}")


# ---------------------------------------------------------
# Plot 2: ACC Timeline
# ---------------------------------------------------------
def plot_acc_timeline(steps, out_dir):
    acc = extract_acc_timeline(steps)

    plt.figure(figsize=(10, 2.5))
    plt.step(range(len(acc)), acc, where="mid", color="#2ca02c", linewidth=2)
    plt.title("ACC Engagement Timeline")
    plt.xlabel("Step Index")
    plt.ylabel("ACC (1=ON, 0=OFF)")
    plt.ylim(-0.2, 1.2)
    plt.grid(True)
    plt.legend(["ACC State"], loc="upper left")

    path = os.path.join(out_dir, "acc_timeline.png")
    plt.savefig(path)
    plt.close()
    print(f"[OK] Saved ACC timeline → {path}")


# ---------------------------------------------------------
# Plot 3: Lane Timeline
# ---------------------------------------------------------
def plot_lane_timeline(steps, out_dir):
    lane = extract_lane_timeline(steps)

    plt.figure(figsize=(10, 3))
    plt.step(range(len(lane)), lane, where="mid", color="#9467bd", linewidth=2)
    plt.title("Lane Position Timeline")
    plt.xlabel("Step Index")
    plt.ylabel("Lane (0=Right, 1=Center, 2=Left)")
    plt.ylim(-0.5, 2.5)
    plt.grid(True)
    plt.legend(["Lane Position"], loc="upper left")

    path = os.path.join(out_dir, "lane_timeline.png")
    plt.savefig(path)
    plt.close()
    print(f"[OK] Saved lane timeline → {path}")


# ---------------------------------------------------------
# Combined function to generate all visualisations
# ---------------------------------------------------------
def generate_all_visualisations(steps, out_dir):
    plot_speed_profile(steps, out_dir)
    plot_acc_timeline(steps, out_dir)
    plot_lane_timeline(steps, out_dir)
