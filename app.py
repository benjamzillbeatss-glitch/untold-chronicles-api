from flask import Flask, jsonify
import pandas as pd

csv_url = "https://drive.google.com/uc?export=download&id=1iCJOa3egMl0Qz7lWyBMFKfk9Dqj1rFDh"

df = pd.read_csv(csv_url, on_bad_lines='skip', encoding='utf-8', quotechar='"')
print("✅ CSV loaded successfully with", len(df), "rows and columns:", list(df.columns))

app = Flask(__name__)

@app.route("/get_archive", methods=["GET"])
def get_archive():
    record = df.sample(1).iloc[0]
    return jsonify({
        "caption": str(record["caption"]),
        "image_url": str(record["google_drive_link"])
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
