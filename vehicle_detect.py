import cv2
from ultralytics import YOLO

# Load model once (faster + safer)
model = YOLO("yolov8n.pt")

def detect_vehicle(video_path):
    cap = cv2.VideoCapture(video_path)

    # No-parking zone (adjust if needed)
    zone_x1, zone_y1 = 100, 150
    zone_x2, zone_y2 = 500, 400

    violation_found = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])

                # vehicle classes (car, motorbike, bus, truck)
                if cls in [2, 3, 5, 7]:

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    # check no-parking zone
                    if zone_x1 < cx < zone_x2 and zone_y1 < cy < zone_y2:
                        violation_found = True

        if violation_found:
            break

    cap.release()

    if violation_found:
        return "🚨 VIOLATION DETECTED - Fine: Rs.200"
    else:
        return "✅ No Violation Detected"