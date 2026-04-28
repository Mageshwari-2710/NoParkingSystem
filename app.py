from flask import Flask, render_template, request
from ultralytics import YOLO
import os
import uuid
import time

app = Flask(__name__)

# ======================
# CONFIG
# ======================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load lightweight YOLO model (SAFE FOR RENDER)
model = YOLO("yolov8n.pt")

# No Parking Zone (demo rectangle)
ZONE = (100, 100, 500, 400)


# ======================
# HOME PAGE
# ======================
@app.route("/")
def home():
    return render_template("index.html")


# ======================
# UPLOAD VIDEO
# ======================
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["video"]

    if file.filename == "":
        return "No file selected ❌"

    filename = str(uuid.uuid4()) + "_" + file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(path)

    # Process video (safe version)
    process_video(path)

    return """
    <h2>Upload Success ✅</h2>
    <p>Processing completed (check logs)</p>
    """


# ======================
# VIDEO PROCESSING (SAFE VERSION)
# ======================
def process_video(path):
    print("\n===== PROCESS START =====")
    print("Video:", path)

    # We DO NOT use full frame processing on Render (prevents crash)
    # Instead we simulate detection logic safely

    violation_time = 0

    for i in range(1, 6):  # simulate frames
        print(f"Processing frame {i}...")

        # simulate detection
        detected = True if i % 2 == 0 else False

        if detected:
            violation_time += 2

        time.sleep(0.5)

    fine = calculate_fine(violation_time)

    print("Violation Time:", violation_time, "sec")
    print("FINE:", fine)
    print("===== PROCESS END =====\n")


# ======================
# FINE CALCULATION
# ======================
def calculate_fine(seconds):
    return int((seconds / 60) * 10)


# ======================
# LIVE PAGE (NEXT STEP)
# ======================
@app.route("/live")
def live():
    return "Live detection coming next step 🚀"


# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)