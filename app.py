from flask import Flask, render_template, request
import os
from vehicle_detect import detect_vehicle
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("video")

    if not file:
        return "No file uploaded"

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    result = detect_vehicle(path)

    return f"""
    <html>
    <body style="text-align:center;font-family:Arial;margin-top:50px;">
        <h2>🚦 Processing Completed</h2>
        <p>{result}</p>
        <a href="/">Go Back</a>
    </body>
    </html>
    """

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)