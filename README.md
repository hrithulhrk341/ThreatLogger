# 🛡️ ThreatLogger: AI-Powered Brute Force Detection SOC Tool

> Developed by **Hrithul Krishna**

ThreatLogger is a lightweight, AI-ready cybersecurity SOC (Security Operations Center) tool designed to monitor SSH brute-force attacks using system logs. It provides real-time alert visualization, email notifications, and a professional web-based dashboard — making it ideal for home labs, SOC training, and research.

---

## 🔍 Features

- ✅ Real-time SSH brute-force detection via `/var/log/auth.log`
- 📊 Beautiful and interactive web-based dashboard (Flask)
- 📈 Dynamic brute-force visualization graph (Seaborn/Matplotlib)
- 📧 Auto email alerts with log files and graph attachment
- 📂 Clean modular file structure (core, app, templates)
- 🔐 Deployable on any Linux SOC lab / VirtualBox / Cloud VM

---

## 📁 Project Structure

ThreatLogger/
│
├── app/ # Flask App Logic
│ ├── init.py
│ ├── routes.py
│ └── utils.py
│
├── core/ # Core SOC Functions
│ ├── parser.py # Parses auth.log
│ ├── visualize.py # Generates graphs
│ └── emailer.py # Sends email alerts
│
├── templates/ # HTML UI Templates
│ ├── index.html
│ └── dashboard.html
│
├── static/ # Graphs & Assets
│ └── alert_graph.png
│
├── main.py # Main script (for debug/testing)
├── app.py # Entry point to run the Flask server
├── config.py # Email config
├── requirements.txt # Python dependencies
└── README.md # You’re here!


---

## 📦 Installation

```bash
git clone https://github.com/hrithulhrk341/ThreatLogger.git
cd ThreatLogger
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo python app.py

Open browser: http://localhost:5000



📧 Email Alert Setup
Edit config.py with your email credentials (preferably app password):

python
Copy code
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"


🧪 Demo Use Case
To simulate a brute-force SSH attempt:

bash
Copy code
sudo tail -n 20 /var/log/auth.log
# Look for "Failed password for invalid user"


🔐 Future Improvements
✅ JWT authentication for dashboard access

🔍 AI model integration for anomaly detection

📦 Dockerize the whole system

📈 Store alerts in SQLite/Elastic DB

✨ Developed By
Hrithul Krishna
Cybersecurity Enthusiast | Aspiring SOC Analyst
