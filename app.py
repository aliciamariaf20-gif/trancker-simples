from flask import Flask, request, jsonify
import os
from video_analyzer import analyze_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Tracker running"

@app.route("/analyze", methods=["POST"])
def analyze():
    video = request.files["video"]
    path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(path)

    result = analyze_video(path)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
