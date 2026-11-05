import fastf1
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib import pyplot as plt
YEAR = 2025
EVENT = "Monza"
SESSION_TYPE = "Q"


def load_session(year, event, session_type):
    fastf1.Cache.configure()
    session = fastf1.get_session(year, event, session_type)
    session.load()
    return session

def get_fastest_lap_telemetry(session):
    fastest_lap = session.laps.pick_fastest()
    telemetry = fastest_lap.get_telemetry()
    return telemetry

def clean_telemetry(telemetry):
    # Remove unnecessary columns
    columns_to_keep = ['X', 'Y', 'Speed']
    cleaned_telemetry = telemetry[columns_to_keep]
    return cleaned_telemetry


def main():
    session = load_session(YEAR, EVENT, SESSION_TYPE)
    telemetry = get_fastest_lap_telemetry(session)
    cleaned_telemetry = clean_telemetry(telemetry)
    print(cleaned_telemetry.head())
    x = cleaned_telemetry['X']
    y = cleaned_telemetry['Y']
    speed = cleaned_telemetry['Speed'].to_numpy()
    #print(x.shape)
    #print(np.array([x,y]).shape)
    '''
        (-1,1,2)
        [
            [[x,y]],
            [[x,y]]
        ]
    
        if it was (-1,2,2)
        [
            [[x,y],[x,y]],
            [[x,y],[x,y]],
        ]
        '''
    #print(np.array([x,y]).T.reshape(-1,1,2).shape)
    points = np.array([x,y]).T.reshape(-1,1,2)
    #print(points.shape)
    #print(points[:-1].shape)
    #print(points[1:].shape)
    segments = np.concatenate((points[:-1],points[1:]),axis = 1)
    #print(segments.shape)
    norm = Normalize(vmin=speed.min(), vmax=speed.max())
    lc = LineCollection(segments, cmap='turbo', norm=norm)
    segment_speed = (speed[:-1] + speed[1:]) / 2  # one value per segment
    #segment_speed = speed[:-1]  # one value per segment
    #print(segment_speed)
    lc.set_array(segment_speed)
    lc.set_linewidth(4)
    #print(segment_speed[0:10])
    #print("Points:", len(points))
    #print("Segments:", len(segments))
    #print("Segment speeds:", len(segment_speed))
    #print("NaNs:", np.isnan(segment_speed).sum())  
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_aspect("equal")
    ax.axis("off")
    fig.colorbar(lc, ax=ax, label="Speed (km/h)")
    ax.set_title("Speed Map of Fastest Lap - 2025 Italian GP (Monza) Qualifying")
    fastest_lap = session.laps.pick_fastest()
    driver = fastest_lap['Driver']
    lap_time = fastest_lap['LapTime'].total_seconds()
    ax.set_title(f"{driver} | Monza 2025 Qualifying | Fastest Lap: {lap_time:.3f} seconds", fontsize=12)    
    fig.savefig("figures/monza_2025_q_speed_map.png", dpi=200, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
