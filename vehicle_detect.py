import cv2
from test_sms import send_sms

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 🔥 YOUR AI MODEL GOES HERE
        vehicle_detected = True  # placeholder

        if vehicle_detected and not detected:
            detected = True

            print("🚗 No Parking Violation Detected")

            owner_number = "+91XXXXXXXXXX"
            message = "🚫 No Parking violation detected. Fine applied."

            send_sms(owner_number, message)

            break

    cap.release()

    # ❌ IMPORTANT: DO NOT USE THIS IN CLOUD
    # cv2.destroyAllWindows()

    return "Processing completed"