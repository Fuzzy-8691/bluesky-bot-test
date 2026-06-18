#!/usr/bin/env python3
import requests
import json
import random
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ===== CONFIG =====
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# =================

groq_client = Groq(api_key=GROQ_API_KEY)

FALLBACK_MESSAGES = [
    "Hello from the bot! 🤖",
    "Just checking in...",
    "Discord + AI = 💙",
    "Automation is fun!",
    "Beep boop!",
]

def generate_message():
    """Generate a human-like message using Groq API."""
    try:
        system_prompt = """You are a friendly, engaging person sharing interesting thoughts in a Discord chat.
        Your messages should:
        - Sound natural and conversational
        - Be under 200 characters
        - Be original and unique each time
        - Can be about technology, creativity, daily life, or random observations
        - Be positive and engaging"""

        user_prompt = "Generate a unique, friendly message for a Discord chat."

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.9,
            max_tokens=100,
        )
        
        message_text = chat_completion.choices[0].message.content.strip()
        print(f"🤖 AI Generated: {message_text}")
        return message_text
        
    except Exception as e:
        print(f"❌ Error generating message: {e}")
        return random.choice(FALLBACK_MESSAGES)

def main():
    print("🔄 Sending message to Discord...")

    message = generate_message()

    # Send message to Discord via webhook
    data = {
        "content": message,
        "username": "AI Bot",
        "avatar_url": "https://i.imgur.com/4M34hi2.png"  # Optional: Custom avatar
    }

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 204:
            print(f"✅ Posted: {message}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        sys.exit(1)

    print("✅ Bot run complete!")

if __name__ == "__main__":
    main()