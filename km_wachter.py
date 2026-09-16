# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernized 2024.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return the percentage of the service interval consumed."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True if the car has consumed >= WARN_AT_PERCENT of its service interval.

    If last_service_km is absent the reading is unknown, so the car is not flagged.
    """
    if "last_service_km" not in car:
        return False
    km_since = car["odometer"] - car["last_service_km"]
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list) -> list:
    """Return IDs of every car that needs a service and print a line for each."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
