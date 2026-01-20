from flask import Flask, request, jsonify
import os
from video_analyzer import analyze_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Tracker running"

@app.route("/track", methods=["POST"])
def track():
    if "video" not in request.files:
        return jsonify({"error": "Nenhum vídeo enviado"}), 400

    video = request.files["video"]
    path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(path)

    result = analyze_video(path)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
