# Pretty Good AI Voice Bot Tester

## Overview

This project is an automated voice bot that simulates a patient calling a medical office. It interacts with the AI agent, records conversations, and helps identify bugs and edge cases.

## Features

* Makes real phone calls using Twilio
* Simulates realistic patient scenarios
* Maintains multi-turn conversations
* Saves transcripts automatically
* Tests edge cases like:

  * Wrong appointment dates
  * Closed office days
  * Insurance questions
  * Medication refills

## Setup

### 1. Clone the repo

```
git clone https://github.com/yourusername/pgai-voice-bot.git
cd pgai-voice-bot
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file based on `.env.example`

### 4. Run the server

```
python src/app.py
```

### 5. Start ngrok

```
ngrok http 5000
```

Update NGROK_URL in `.env`

### 6. Run a scenario

```
python src/call_agent.py 3
```

## Transcripts

All conversations are saved in the `/transcripts` folder.

## Scenarios Tested

* Appointment scheduling
* Rescheduling
* Medication refill
* Office hours
* Closed day booking
* Insurance coverage
* Location and directions
* Confusing/unclear patient behavior
* Interruptions
* Mid-call changes

## Notes

This bot is designed to uncover weaknesses in conversational AI systems through realistic interactions and edge cases.
