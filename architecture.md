# Architecture

This system uses a Flask server to handle voice interactions via Twilio.

When a call is initiated, Twilio sends a webhook request to the `/voice` endpoint, which starts the conversation. User speech is captured and sent to `/handle-speech`, where it is processed.

The system uses OpenAI's API to generate realistic patient responses based on predefined scenarios. Conversation history is maintained to support multi-turn interactions.

Each call is logged and saved as a transcript for later analysis. The design prioritizes simplicity, reliability, and fast iteration for testing conversational edge cases.
