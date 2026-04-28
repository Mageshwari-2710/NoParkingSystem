import os
import cv2
import time
import mysql.connector
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

model = YOLO("best.pt")

FINE_PER_SECOND = 5
VIOLATION_THRESHOLD = 5  # seconds


# ---------------- MYSQL ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Magi@123",
    database="noparking"
)
cursor = db.cursor()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("video")
    if not file:
        return "No video uploaded"

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    process_video(path, filename)

    return "Processing done & stored in database!"


# ---------------- VIDEO PROCESS ----------------
def process_video(video_path, video_name):

    cap = cv2.VideoCapture(video_path)

    entry_time = {}
    saved = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        now = time.time()

        h, w = frame.shape[:2]

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:

                cls = int(box.cls[0])
                label = model.names[cls]

                if label not in ["car", "motorcycle", "truck"]:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # ---------------- NO PARKING REGION ----------------
                # (bottom 40% of frame)
                if y2 > h * 0.6:

                    vehicle_id = f"{label}_{x1}_{y1}"

                    # ENTRY TIME
                    if vehicle_id not in entry_time:
                        entry_time[vehicle_id] = now

                    duration = now - entry_time[vehicle_id]

                    # VIOLATION DETECTED
                    if duration > VIOLATION_THRESHOLD and vehicle_id not in saved:

                        fine = duration * FINE_PER_SECOND

                        save_to_db(
                            vehicle_id,
                            entry_time[vehicle_id],
                            now,
                            duration,
                            fine,
                            video_name
                        )

                        saved.add(vehicle_id)

                else:
                    # vehicle left zone
                    vehicle_id = f"{label}_{x1}_{y1}"
                    entry_time.pop(vehicle_id, None)

    cap.release()


# ---------------- SAVE TO DB ----------------
def save_to_db(vehicle_id, entry, exit_t, duration, fine, video_name):

    sql = """
    INSERT INTO violations
    (vehicle_id, entry_time, exit_time, duration, fine, video_name)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (vehicle_id, entry, exit_t, duration, fine, video_name)

    cursor.execute(sql, values)
    db.commit()


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)