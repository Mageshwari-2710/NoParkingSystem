from flask import Flask, render_template, request
from ultralytics import YOLO
import cv2
import os
import uuid
import time

app = Flask(__name__)

# =========================
# CONFIG
# =========================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLO ONCE (IMPORTANT FOR RENDER)
model = YOLO("yolov8n.pt")

# No Parking Zone (x1, y1, x2, y2)
NO_PARKING_ZONE = (100, 100, 500, 400)


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# UPLOAD VIDEO
# =========================
@app.route("/upload", methods=["POST"])
def upload_video():
    file = request.files["video"]

    if file.filename == "":
        return "No file selected ❌"

    filename = str(uuid.uuid4()) + "_" + file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    # PROCESS VIDEO
    process_video(path)

    return f"""
    <h2>Upload Successful ✅</h2>
    <p>File: {filename}</p>
    <p>Processing Done 🚀 Check server logs</p>
    """


# =========================
# FINE CALCULATION
# =========================
def calculate_fine(seconds):
    rate_per_minute = 10
    minutes = seconds / 60
    return int(minutes * rate_per_minute)


# =========================
# CORE DETECTION FUNCTION
# =========================
def process_video(video_path):

    cap = cv2.VideoCapture(video_path)

    violation_start_time = None
    total_violation_time = 0

    x1, y1, x2, y2 = NO_PARKING_ZONE

    print("\n========== PROCESS START ==========")
    print("Video:", video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # YOLO detection
        results = model(frame)

        vehicle_in_zone = False

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                if label in ["car", "motorbike", "bus", "truck"]:
                    x1b, y1b, x2b, y2b = box.xyxy[0]
                    cx = int((x1b + x2b) / 2)
                    cy = int((y1b + y2b) / 2)

                    # Check if inside no-parking zone
                    if x1 < cx < x2 and y1 < cy < y2:
                        vehicle_in_zone = True

        # TIME TRACKING
        if vehicle_in_zone:
            if violation_start_time is None:
                violation_start_time = time.time()
        else:
            if violation_start_time is not None:
                total_violation_time += time.time() - violation_start_time
                violation_start_time = None

    cap.release()

    # Final calculation
    fine = calculate_fine(total_violation_time)

    print("========== RESULT ==========")
    print("Total Violation Time (sec):", total_violation_time)
    print("Fine Amount:", fine)
    print("========== END ==========\n")


# =========================
# LIVE PAGE (NEXT STEP)
# =========================
@app.route("/live")
def live():
    return "Live detection will be added in next step 🚀"


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)