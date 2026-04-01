from twilio.rest import Client
from dotenv import load_dotenv
import os
import sys

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ---------------------------
# Phone numbers
# ---------------------------
FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")   # your Twilio number
TO_NUMBER = "+18054398008"  # required test number


# ---------------------------
# Make call
# ---------------------------
def make_call(scenario):
    ngrok_url = os.getenv("NGROK_URL")

    if not ngrok_url:
        print("❌ NGROK_URL not set in .env")
        return

    url = f"{ngrok_url}/voice?scenario={scenario}"

    print("\n📞 Starting call...")
    print("Scenario:", scenario)
    print("Webhook URL:", url)

    try:
        call = client.calls.create(
            to=TO_NUMBER,
            from_=FROM_NUMBER,
            url=url
        )

        print("✅ Call started successfully!")
        print("Call SID:", call.sid)

    except Exception as e:
        print("❌ Error making call:")
        print(e)


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        scenario = sys.argv[1]
    else:
        scenario = "0"

    print("Running scenario:", scenario)
    make_call(scenario)