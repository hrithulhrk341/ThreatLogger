from flask import Blueprint, render_template, request
import pandas as pd
import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from flask_mail import Message
from . import mail

main = Blueprint("main", __name__)

AUTH_LOG_PATH = "/var/log/auth.log"
ALERT_FILE = "alerts.txt"
GRAPH_FILE = "static/alert_graph.png"

def parse_log_file():
    failed_attempts = []

    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*Failed password for invalid user (\S+) from (\S+)"

    if os.path.exists(AUTH_LOG_PATH):
        with open(AUTH_LOG_PATH, "r") as log:
            for line in log:
                match = re.search(pattern, line)
                if match:
                    timestamp, user, ip = match.groups()
                    failed_attempts.append({
                        "Timestamp": timestamp,
                        "Username": user,
                        "IP": ip
                    })
    
    return pd.DataFrame(failed_attempts)

def save_alerts(df):
    df.to_csv(ALERT_FILE, index=False, sep="\t")

def generate_graph(df):
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna()

    if not df.empty:
        df["Time"] = df["Timestamp"].dt.floor("min")
        plot = sns.countplot(data=df, x="Time", palette="Reds")
        plt.xticks(rotation=45, ha='right')
        plt.title("Brute Force Attempt Timeline")
        plt.tight_layout()
        plt.savefig(GRAPH_FILE)
        plt.clf()

def send_email_alert(df):
    if not df.empty:
        message = Message("🚨 ThreatLogger Alert - Brute Force Attempts Detected",
                          recipients=[os.getenv("ALERT_RECEIVER")])
        message.body = f"""
🚨 Brute Force Attempts Detected

Total Attempts: {len(df)}

Recent Attempts:
{df.tail(5).to_string(index=False)}

Check the dashboard for full details.
"""
        with open(GRAPH_FILE, "rb") as img:
            message.attach("alert_graph.png", "image/png", img.read())

        mail.send(message)

@main.route("/")
def dashboard():
    df = parse_log_file()

    if not df.empty:
        save_alerts(df)
        generate_graph(df)
        send_email_alert(df)

    return render_template("dashboard.html", data=df.to_dict(orient="records"), graph=GRAPH_FILE)
