from flask import Flask, request, session
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask_session import Session
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

# ---------------------------
# Setup
# ---------------------------
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = OpenAI()

# ---------------------------
# Transcripts
# ---------------------------
TRANSCRIPT_DIR = "transcripts"

if not os.path.exists(TRANSCRIPT_DIR):
    os.makedirs(TRANSCRIPT_DIR)


def save_transcript(conversation, scenario):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{TRANSCRIPT_DIR}/transcript-{scenario}-{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for line in conversation:
            f.write(line + "\n")

    print(f"📁 Saved transcript: {filename}")


# ---------------------------
# Scenarios (Patient behavior)
# ---------------------------
SCENARIOS = {
    "0": "You are a patient trying to book a normal appointment.",
    "1": "You are a patient trying to reschedule an appointment.",
    "2": "You are a patient asking about office hours.",
    "3": "You are a patient requesting a medication refill.",
    "4": "You are a patient being confused and give unclear answers.",
    "5": "You are a patient who interrupt the agent frequently.",
    "6": "You believe your appointment date is wrong and want to fix it.",
    "7": "You are a patient trying to book an appointment on weekends.",
    "8": "You are asking whether your insurance is accepted and what is covered.",
    "9": "You are asking for the clinic location and directions.",
    "10": "asking for urgent same-day appointment availability."
}


# ---------------------------
# GPT response (Patient side)
# ---------------------------
def generate_patient_response(agent_input, scenario, history):
    system_prompt = f"""
    You are a patient on a phone call with a medical office.


    Scenario:
    {SCENARIOS.get(str(scenario), "")}
    """

    messages = [
        {"role": "system", "content": f"You are a patient.\n{system_prompt}"}
    ]

    # include conversation history
    for msg in history[-10:]:
        if msg.startswith("AGENT:"):
            messages.append({"role": "user", "content": msg.replace("AGENT: ", "")})
        elif msg.startswith("PATIENT:"):
            messages.append({"role": "assistant", "content": msg.replace("PATIENT: ", "")})

    # latest agent input
    messages.append({"role": "user", "content": agent_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content


# ---------------------------
# Start call
# ---------------------------
@app.route("/voice", methods=["POST"])
def voice():
    scenario = request.args.get("scenario", "0")

    session["scenario"] = scenario
    session["conversation"] = []

    print("START CALL - SCENARIO:", scenario)

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/handle-speech",
        method="POST",
        timeout = 5,
        speechTimeout = "auto"
    )

    gather.say("Hello, I am calling about my appointment.")
    response.append(gather)

    return str(response)


# ---------------------------
# Handle conversation
# ---------------------------
@app.route("/handle-speech", methods=["POST"])
def handle_speech():
    agent_input = request.form.get("SpeechResult", "")
    scenario = session.get("scenario", "0")
    conversation = session.get("conversation", [])

    print("AGENT:", agent_input)

    # Save agent input
    conversation.append(f"AGENT: {agent_input}")

    # Generate patient reply
    patient_reply = generate_patient_response(agent_input, scenario, conversation)

    print("PATIENT:", patient_reply)

    conversation.append(f"PATIENT: {patient_reply}")
    session["conversation"] = conversation

    response = VoiceResponse()

    # ---------------------------
    # Ending condition
    # ---------------------------
    if (
        "goodbye" in patient_reply.lower()
        or "thank you" in patient_reply.lower()
        or len(conversation) > 20
    ):
        save_transcript(conversation, scenario)
        response.say("Thank you, goodbye.")
        response.hangup()
        return str(response)

    # ---------------------------
    # Continue conversation
    # ---------------------------
    gather = Gather(
        input="speech",
        action="/handle-speech",
        method="POST",
        timeout = 5,
        speechTimeout = "auto"
    )

    gather.say(patient_reply)
    response.append(gather)

    response.say("I didn't catch that. Let me try again.")
    response.redirect("/handle-speech")

    return str(response)


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)