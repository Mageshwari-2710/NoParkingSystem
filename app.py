import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    from ultralytics import YOLO  # ✅ LOAD INSIDE ROUTE (IMPORTANT)

    model = YOLO("best.pt")       # ✅ prevents Render startup crash

    file = request.files.get("video")
    if not file:
        return "No file uploaded"

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    import cv2
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
    <p>Frames: {frames}</p>
    <p>Violations: {violations}</p>
    <h2>Fine: ₹{fine}</h2>
    """


# IMPORTANT FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)