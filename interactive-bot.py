#!/usr/bin/env python3
import os
import random
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from groq import Groq

load_dotenv()

# ===== CONFIG =====
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# =================

groq_client = Groq(api_key=GROQ_API_KEY)

# --- Set up bot with only the intents you need ---
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Fallback responses ---
FALLBACK_RESPONSES = [
    "I'm thinking... 🤔",
    "Good question!",
    "Let me get back to you on that.",
    "I'm not sure, but I'm learning!",
]

# --- AI Response Function ---
def get_ai_response(prompt):
    """Generate a response using Groq API."""
    try:
        system_prompt = """You are a friendly, helpful AI assistant in a Discord server.
        Your responses should be:
        - Conversational and natural
        - Under 500 characters
        - Helpful and engaging
        - Appropriate for all ages"""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=200,
        )
        
        return chat_completion.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return random.choice(FALLBACK_RESPONSES)

# --- Commands ---

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    print(f"✅ Connected to {len(bot.guilds)} server(s)")

@bot.command()
async def hello(ctx):
    """Say hello!"""
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

@bot.command()
async def joke(ctx):
    """Tell a random joke."""
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "What do you call a snake that builds computers? A python! 🐍",
        "Why did the developer go broke? Because he used up all his cache! 💰",
        "What's a computer's favorite snack? Microchips! 🍟",
        "Why do Java developers wear glasses? Because they can't C#! 👓",
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def ai(ctx, *, prompt):
    """Ask the AI a question! Usage: !ai <your question>"""
    await ctx.send(f"🧠 Thinking...")
    
    response = get_ai_response(prompt)
    await ctx.send(response)

# --- Error Handling for !ai command ---
@ai.error
async def ai_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ **Please provide a question!**\nExample: `!ai What is 2+2?`")
    else:
        await ctx.send(f"❌ An error occurred: {error}")

@bot.command()
async def ping(ctx):
    """Check bot latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms")

@bot.command()
async def helpme(ctx):
    """Show all available commands."""
    help_text = """
**🤖 Available Commands:**
`!hello` - Say hello
`!joke` - Tell a random joke
`!ai <question>` - Ask the AI a question
`!ping` - Check bot latency
`!helpme` - Show this menu
"""
    await ctx.send(help_text)

# --- Run the bot ---
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)