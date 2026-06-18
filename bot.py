#!/usr/bin/env python3
import time
import random
import sys
import os
from atproto import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===== CONFIG =====
HANDLE = os.getenv("BLUESKY_HANDLE")
PASSWORD = os.getenv("BLUESKY_PASSWORD")
# =================

POSTS = [
    "Just a bot living in the matrix 🤖",
    "Beep boop, another day, another post",
    "I post so you don't have to",
    "Automation is my middle name",
    "🌊 Riding the algorithmic waves",
    "Just vibing on Bluesky",
    "Hello from the other side of the internet",
    "This post was brought to you by a Python script",
    "Do androids dream of electric sheep? I dream of likes",
    "No thoughts, just vibes",
    "I'm not a human, I'm a posting machine",
    "Here's your scheduled dose of internet",
    "Bluesky > Blue sky? Both are great",
    "Posting autonomously since 2026",
    "My code runs, therefore I post",
    "Did you know this post was scheduled?",
    "The sky's not the limit, it's the platform",
    "I speak fluent Python and sarcasm",
    "Automating my way through the internet",
    "Who needs a social media manager? Just use a bot!",
]

print("🔄 Logging in...")
client = Client()
client.login(HANDLE, PASSWORD)
print("✅ Logged in successfully!")

post_count = 0
while True:
    post = random.choice(POSTS)
    try:
        client.send_post(post)
        post_count += 1
        print(f"✅ [#{post_count}] Posted: {post}")
        sys.stdout.flush()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.stdout.flush()
    
    time.sleep(14400)  # 4 hours
