import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

log_file_path = "/var/log/auth.log"
alert_txt_path = "alerts.txt"
alert_json_path = "alerts.json"
alert_png_path = "static/alert_graph.png"  # Save inside static for Flask access

def parse_auth_log():
    pattern = re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.\d+.*?Failed password for invalid user (?P<username>\w+) from (?P<ip>[\d.:a-fA-F]+)"
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
                alerts.append({"Timestamp": timestamp, "Username": username, "IP": ip})

    return pd.DataFrame(alerts)

def save_alerts(df):
    if df.empty:
        print("\n📄 No alerts to save.")
        return

    df.to_csv(alert_txt_path, index=False, sep=' ')
    df.to_json(alert_json_path, orient="records", date_format="iso")
    print(f"\n📄 Alerts saved to: {alert_txt_path}")

    # Plot
    plt.figure(figsize=(10, 5))
    df["Hour"] = df["Timestamp"].dt.floor("h")
    sns.countplot(data=df, x="Hour", color='red')
    plt.title("Brute Force Attempts Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(alert_png_path)
    print(f"🖼 Graph saved to: {alert_png_path}")

if __name__ == "__main__":
    df = parse_auth_log()
    if df.empty:
        print("\n📉 No failed login attempts found in logs.")
    else:
        print("\n🚨 Possible Brute-Force Attacks Detected:\n")
        print(df[["Timestamp", "Username", "IP"]])
        save_alerts(df)

