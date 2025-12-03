from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

# ---------------------------
# EXISTING NICHE (do not touch)
# ---------------------------

csv_url = "https://drive.google.com/uc?export=download&id=1iCJOa3egMl0Qz7lWyBMFKfk9Dqj1rFDh"

df = pd.read_csv(csv_url, on_bad_lines='skip', encoding='utf-8', quotechar='"')
print("✅ CSV loaded successfully with", len(df), "rows and columns:", list(df.columns))

@app.route("/get_archive", methods=["GET"])
def get_archive():
    record = df.sample(1).iloc[0]
    return jsonify({
        "caption": str(record["caption"]),
        "image_url": str(record["google_drive_link"])
    })


# ---------------------------
# NEW NICHES FROM LOCAL /data
# ---------------------------

def load_local_csv(filename):
    path = os.path.join("data", filename)
    try:
        df = pd.read_csv(path, on_bad_lines='skip', encoding='utf-8', quotechar='"')
        print(f"Loaded {filename} — {len(df)} rows")
        return df
    except Exception as e:
        print(f"Failed to load {filename}: {e}")
        return None


datasets = {
    "history": load_local_csv("HISTORY.csv"),
    "historycolored": load_local_csv("history_colored.csv"),
    "nasa": load_local_csv("NASA.csv"),
    "nasa2": load_local_csv("NASA_2.csv"),
    "natgeo": load_local_csv("NATGEOTRAVEL.csv")
}

@app.route("/niche/<name>", methods=["GET"])
def get_niche_random(name):
    if name not in datasets or datasets[name] is None:
        return jsonify({"error": "Niche not found"}), 404

    df = datasets[name]
    record = df.sample(1).iloc[0]

    return jsonify({
        "caption": str(record["caption"]),
        "image_url": str(record["google_drive_link"])
    })


# ---------------------------
# SERVER START — MUST BE LAST
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
