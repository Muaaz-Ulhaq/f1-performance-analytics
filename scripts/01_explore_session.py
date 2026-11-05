"""Explore one FastF1 session: top 10, fastest lap, telemetry channels, deleted laps.

Session: 2025 Italian Grand Prix (Monza), Qualifying.
"""

import fastf1

YEAR = 2025
EVENT = "Monza"
SESSION_TYPE = "Q"


def load_session(year, event, session_type):
    # Note: enable_cache is deprecated in newer FastF1; Cache.configure replaces it.
    fastf1.Cache.enable_cache("cache")
    session = fastf1.get_session(year, event, session_type)
    session.load()
    return session


def print_top_ten(session):
    print("Top 10 by Q3 time")
    print(session.results.iloc[0:10].loc[:, ["Abbreviation", "Q3"]])


def summarise_fastest_lap(session):
    fastest = session.laps.pick_fastest()
    print(f"\nFastest lap: {fastest['Driver']} - {fastest['LapTime']}")

    telemetry = fastest.get_telemetry()
    print(f"Telemetry: {telemetry.shape[0]} rows x {telemetry.shape[1]} columns")
    print(list(telemetry.columns))


def summarise_deleted_laps(session):
    laps = session.laps
    deleted = laps[laps["Deleted"] == True]  # noqa: E712

    print(f"\nDeleted laps: {len(deleted)}")
    print(deleted[["Driver", "LapNumber", "LapTime", "DeletedReason"]])


def main():
    session = load_session(YEAR, EVENT, SESSION_TYPE)
    print_top_ten(session)
    summarise_fastest_lap(session)
    summarise_deleted_laps(session)


if __name__ == "__main__":
    main()