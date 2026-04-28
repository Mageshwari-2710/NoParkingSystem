import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_sms(to_number, message):
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone = os.getenv("TWILIO_PHONE")

    if not account_sid or not auth_token or not twilio_phone:
        print("❌ Twilio environment variables missing")
        return

    try:
        client = Client(account_sid, auth_token)

        msg = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=to_number
        )

        print("✅ SMS sent:", msg.sid)

    except Exception as e:
        print("❌ SMS Error:", e)