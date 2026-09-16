# log_util.py
# Minimal logger for KM-Waechter. Modernized 2024.

import time

LOG_LINES: list[str] = []


def log(message: str) -> None:
    """Append a timestamped line to the in-memory log and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def flush_log(path: str) -> None:
    """Write buffered log lines to the given file and clear the buffer."""
    with open(path, "a", encoding="utf-8") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
