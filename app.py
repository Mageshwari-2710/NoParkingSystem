from flask import Flask, render_template, request
import os
import cv2
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load model ONCE (important for Render)
model = YOLO("best.pt")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("video")

    if not file:
        return "No file uploaded"

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    cap = cv2.VideoCapture(path)

    frames = 0
    violations = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frames += 1

        results = model(frame)

        for r in results:
            if r.boxes is not None:
                violations += len(r.boxes)

    cap.release()

    fine = violations * 100

    return f"""
    <h2>Result</h2>
    <p>Total Frames: {frames}</p>
    <p>Violations: {violations}</p>
    <h3>Fine: ₹{fine}</h3>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)