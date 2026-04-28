from flask import Flask, render_template, request
import os
import uuid

app = Flask(__name__)

# Folder to store uploaded videos
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# HOME PAGE (UI)
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# UPLOAD VIDEO
# =========================
@app.route("/upload", methods=["POST"])
def upload_video():
    try:
        file = request.files["video"]

        if file.filename == "":
            return "No file selected ❌"

        # Create unique filename (important for Render)
        filename = str(uuid.uuid4()) + "_" + file.filename
        path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(path)

        # STEP 4: PROCESS HOOK (NO YOLO YET)
        process_video(path)

        return f"""
        Video uploaded successfully ✅<br>
        File: {filename}<br>
        Processing started 🚀
        """

    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# STEP 4: VIDEO PROCESS FUNCTION (SAFE PLACEHOLDER)
# =========================
def process_video(video_path):
    print("===================================")
    print("VIDEO RECEIVED FOR PROCESSING")
    print("Path:", video_path)
    print("===================================")

    # IMPORTANT:
    # We will add:
    # - OpenCV frame reading
    # - YOLO detection
    # - No-parking zone logic
    # - Fine calculation
    # - Twilio SMS
    #
    # in next steps


# =========================
# LIVE PAGE (PLACEHOLDER)
# =========================
@app.route("/live")
def live():
    return "Live detection will be added in STEP 5 🚀"


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)