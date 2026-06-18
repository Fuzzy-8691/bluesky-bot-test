#!/usr/bin/env python3
import time
import random
import sys
import os
from atproto import Client
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# ===== CONFIG =====
HANDLE = os.getenv("BLUESKY_HANDLE")
PASSWORD = os.getenv("BLUESKY_PASSWORD")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# =================

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY)
bsky_client = Client()

# Fallback posts (in case Groq API fails)
FALLBACK_POSTS = [
    "Just a bot living in the matrix 🤖",
    "Beep boop, another day, another post",
    "I post so you don't have to",
    "Automation is my middle name",
    "🌊 Riding the algorithmic waves",
    "Just vibing on Bluesky",
]

def generate_post():
    """Generate a human-like post using Groq API."""
    try:
        system_prompt = """You are a thoughtful, creative person sharing brief, interesting thoughts on Bluesky. 
        Your posts should be:
        - Under 300 characters
        - Sound natural and human
        - Avoid hashtags
        - Be original and unique each time
        - Can be about technology, creativity, daily life, or random observations"""
        
        user_prompt = "Generate a unique, human-sounding post for Bluesky."

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.9,
            max_tokens=100,
        )
        
        post_text = chat_completion.choices[0].message.content.strip()
        print(f"🤖 AI Generated: {post_text}")
        return post_text
        
    except Exception as e:
        print(f"❌ Error generating post: {e}")
        # Fallback to random static post
        return random.choice(FALLBACK_POSTS)

def main():
    """Main bot function - posts once and exits."""
    print("🔄 Logging in to Bluesky...")
    bsky_client.login(HANDLE, PASSWORD)
    print("✅ Logged in successfully!")

    # Generate and send a post
    post_text = generate_post()
    try:
        bsky_client.send_post(post_text)
        print(f"✅ Posted: {post_text}")
    except Exception as e:
        print(f"❌ Error sending post: {e}")
        sys.exit(1)

    print("✅ Bot run complete!")

if __name__ == "__main__":
    main()