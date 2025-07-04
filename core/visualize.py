import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def generate_graph(alerts):
    if alerts.empty:
        print("No data to plot.")
        return
    
    sns.set(style="darkgrid")
    plt.figure(figsize=(12, 6))
    sns.countplot(x="Timestamp", data=alerts)
    plt.xticks(rotation=45)
    plt.title("Brute Force Attack Attempts Over Time")
    plt.tight_layout()

    # Save to static folder
    output_path = os.path.join("static", "alert_graph.png")
    plt.savefig(output_path)
    plt.close()
    print(f"🖼 Graph saved to: {output_path}")
