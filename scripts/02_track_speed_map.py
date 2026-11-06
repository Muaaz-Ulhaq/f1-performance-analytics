"""Plot the fastest qualifying lap as a track map coloured by speed.

Session: 2025 Italian Grand Prix (Monza), Qualifying.
Output: figures/monza_2025_q_speed_map.png
"""

from pathlib import Path

import fastf1
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.colors import LinearSegmentedColormap

YEAR = 2025
EVENT = "Monza"
SESSION_TYPE = "Q"
OUTPUT_DIR = Path("figures")


def load_session(year, event, session_type):
    fastf1.Cache.configure()  # uses FastF1's default cache location
    session = fastf1.get_session(year, event, session_type)
    session.load()
    return session


def build_colored_segments(x, y, speed):
    """Split a path into segments, with one speed value per segment."""
    points = np.array([x, y]).T.reshape(-1, 1, 2)                 # (N, 1, 2)
    segments = np.concatenate((points[:-1], points[1:]), axis=1)  # (N-1, 2, 2)
    segment_speed = (speed[:-1] + speed[1:]) / 2                  # (N-1,)
    return segments, segment_speed


def format_lap_time(lap_time):
    minutes, seconds = divmod(lap_time.total_seconds(), 60)
    return f"{int(minutes)}:{seconds:06.3f}"


def plot_speed_map(telemetry, title):
    x = telemetry["X"].to_numpy()
    y = telemetry["Y"].to_numpy()
    speed = telemetry["Speed"].to_numpy()

    segments, segment_speed = build_colored_segments(x, y, speed)

    norm = Normalize(vmin=speed.min(), vmax=speed.max())
    speed_cmap = LinearSegmentedColormap.from_list("speed", ["red", "yellow", "green"])
    line_collection = LineCollection(segments, cmap=speed_cmap, norm=norm)
    line_collection.set_array(segment_speed)
    line_collection.set_linewidth(4)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.add_collection(line_collection)
    ax.autoscale()
    ax.set_aspect("equal")  # keep the circuit's true proportions
    ax.axis("off")
    fig.colorbar(line_collection, ax=ax, label="Speed (km/h)")
    ax.set_title(title, fontsize=12)
    return fig


def main():
    session = load_session(YEAR, EVENT, SESSION_TYPE)

    fastest_lap = session.laps.pick_fastest()
    telemetry = fastest_lap.get_telemetry()

    title = (
        f"{fastest_lap['Driver']} | {EVENT} {YEAR} Qualifying | "
        f"Fastest lap {format_lap_time(fastest_lap['LapTime'])}"
    )
    fig = plot_speed_map(telemetry, title)

    #OUTPUT_DIR.mkdir(exist_ok=True)
    #fig.savefig(OUTPUT_DIR / "monza_2025_q_speed_map.png", dpi=200, bbox_inches="tight")
    #plt.show()
    circuit_info = session.get_circuit_info()
    #print(circuit_info.columns)
    corners = circuit_info.corners
    #print(corners.head())

    ax = fig.axes[0]
    for _, row in corners.iterrows():
        x = row["X"]
        y = row["Y"]
        number = row["Number"]
        print(f"Corner {number}: X={x}, Y={y}")    
        ax.text(x,y,str(number), ha="right", va="bottom", fontsize=10, color="black")

    OUTPUT_DIR.mkdir(exist_ok=True)
    fig.savefig(OUTPUT_DIR / "monza_2025_q_speed_map.png", dpi=200, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()