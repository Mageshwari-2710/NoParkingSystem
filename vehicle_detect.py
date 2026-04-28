from dotenv import load_dotenv
load_dotenv()

import cv2
from test_sms import send_sms

def detect_vehicle(video_path):
    cap = cv2.VideoCapture(video_path)

    violation_sent = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # ------------------------
        # YOUR MODEL LOGIC HERE
        # ------------------------
        vehicle_detected = True

        if vehicle_detected and not violation_sent:
            print("🚗 Violation detected")

            owner_number = "+91XXXXXXXXXX"
            message = "🚫 No Parking Violation detected"

            send_sms(owner_number, message)

            violation_sent = True
            break

    cap.release()

    # IMPORTANT: NO cv2.imshow, NO destroyAllWindows

    return "Processed Successfully"