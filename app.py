from flask import Flask, render_template, send_file
from core.parser import parse_auth_log
from core.visualize import generate_graph
from core.emailer import send_email
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Parse log file and get alerts as DataFrame
    df = parse_auth_log()

    # DEBUG: print parsed alerts
    print("\n🚨 Parsed Alerts DataFrame:\n", df)

    # Save alerts
    df.to_csv("alerts.txt", index=False)
    df.to_json("alerts.json", orient="records", date_format="iso")

    # Generate graph
    generate_graph(df)

    # Send email
    if not df.empty:
        send_email(
            subject="🚨 Brute-Force Attack Detected on SSH",
            body="Brute-force login attempts were detected. See attached files.",
            attachments=["alerts.txt", "static/alert_graph.png"]
        )

    # DEBUG: check what's being passed to template
    print("\n🚨 Alerts Sent to Template:\n", df.to_dict(orient="records"))

    return render_template("index.html", alerts=df.to_dict(orient="records"))

# ✅ FIX: This route is REQUIRED to show the graph
@app.route("/graph")
def get_graph():
    graph_path = os.path.join("static", "alert_graph.png")
    if os.path.exists(graph_path):
        return send_file(graph_path, mimetype="image/png")
    else:
        return "Graph not found. Run parser first.", 404

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True, port=5000)
