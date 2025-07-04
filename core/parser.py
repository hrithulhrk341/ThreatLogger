import re
import pandas as pd
from datetime import datetime

log_file_path = "/var/log/auth.log"

def parse_auth_log():
    pattern = re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})[^\n]*?Failed password for invalid user (?P<username>[\w\-]+) from (?P<ip>[\d.:]+)"
    )

    alerts = []

    with open(log_file_path, "r") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                timestamp_str = match.group("timestamp")
                username = match.group("username")
                ip = match.group("ip")
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    timestamp = None
                alerts.append({
                    "Timestamp": timestamp,
                    "Username": username,
                    "IP": ip
                })

    return pd.DataFrame(alerts)
