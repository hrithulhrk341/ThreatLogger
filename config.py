import os

LOG_FILE = "/var/log/auth.log"
ALERT_FILE = "alerts/alerts.txt"
ALERT_GRAPH = "static/alert_graph.png"

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_RECEIVER = "receiver_email@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Use .env
