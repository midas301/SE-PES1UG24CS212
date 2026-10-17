"""Maintenance tracker for telecom towers."""
import sqlite3

CONN = sqlite3.connect(":memory:")
CONN.execute(
    "CREATE TABLE towers (id INTEGER PRIMARY KEY, site TEXT, "
    "last_service INTEGER, faults INTEGER)"
)
STATS = {"service_count": 0}
FAULT_THRESHOLD = 3
OVERDUE_YEARS = 2


def add_tower(site, last_service, faults=0):
    """Insert a new tower using a parameterized query."""
    CONN.execute(
        "INSERT INTO towers (site, last_service, faults) VALUES (?, ?, ?)",
        (site, last_service, faults),
    )
    CONN.commit()


def service_tower(tower_id, year):
    """Record a service visit and reset the tower's fault count."""
    try:
        CONN.execute(
            "UPDATE towers SET last_service = ?, faults = 0 WHERE id = ?",
            (year, tower_id),
        )
        CONN.commit()
        STATS["service_count"] += 1
    except sqlite3.Error as err:
        print(f"service failed: {err}")


def overdue(year):
    """Return the sites not serviced for OVERDUE_YEARS or more."""
    rows = CONN.execute("SELECT site, last_service FROM towers").fetchall()
    return [site for site, last in rows if year - last >= OVERDUE_YEARS]


def risk_level(tower_id):
    """Return 'high' if the tower has many faults, otherwise 'normal'."""
    row = CONN.execute(
        "SELECT faults FROM towers WHERE id = ?", (tower_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"Unknown tower id: {tower_id}")
    return "high" if row[0] > FAULT_THRESHOLD else "normal"


def snapshot():
    """Return all tower rows."""
    return CONN.execute("SELECT * FROM towers").fetchall()


def main():
    """Run a short demonstration."""
    add_tower("Ridge-A", 2021, 5)
    add_tower("Coast-B", 2024)
    service_tower(2, 2025)
    total = len(snapshot())
    print(overdue(2025), risk_level(1), total, STATS["service_count"])


if __name__ == "__main__":
    main()
