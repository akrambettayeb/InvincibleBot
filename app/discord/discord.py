import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from app.chatgpt.openai import chatgpt_response
import random
import itertools
from itertools import *
import json
import asyncio

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NUM_EPISODES = 16


def get_prefix(client, message):
    s = "mark "
    prefixes = list(map("".join, itertools.product(*zip(s.upper(), s.lower()))))
    return commands.when_mentioned_or(*prefixes)(client, message)


status = cycle(
    [
        discord.Game(name="Catch with Dad"),
        discord.Activity(type=discord.ActivityType.watching, name="INVINCIBLE"),
    ]
)

# File name for storing invincibleCounters
COUNTER_FILE = "invincibleCounters.json"

# Check if the file exists and read the value
if os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "r") as file:
        invincibleCounters = json.load(file)
else:
    invincibleCounters = {}

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)


@client.event
async def on_ready():
    print("Hello, bot is ready")
    change_status.start()
    await client.change_presence(status=discord.Status.do_not_disturb)


@tasks.loop(minutes=1)
async def change_status():
    await client.change_presence(activity=next(status))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    guild_id = str(message.guild.id)  # Convert to string for JSON serialization

    # Initialize the counter for the guild if it doesn't exist
    if guild_id not in invincibleCounters:
        invincibleCounters[guild_id] = 0

    play = False
    for word in message.content.lower().split():
        if "invincible" in word or client.user.mentioned_in(message):
            play = True
            invincibleCounters[guild_id] += 1

    # Save the updated invincibleCounters to the file
    with open(COUNTER_FILE, "w") as file:
        json.dump(invincibleCounters, file)

    switch = {}
    for i in range(NUM_EPISODES):
        switch[i] = f"title_cards/Invincible{i+1}.mp4"
    if play:
        await message.channel.send(
            file=discord.File(
                switch.get(
                    (invincibleCounters[guild_id] - 1) % NUM_EPISODES, "No such file"
                )
            )
        )
    command, user_message = None, None
    for text in ["/invincible", "/invinciblebot", "/mark", "/markbot"]:
        if message.content.startswith(text):
            command = message.content.split(" ")[0]
            user_message = message.content.replace(text, "")

    if (
        command == "/invincible"
        or command == "/invinciblebot"
        or command == "/mark"
        or command == "/markbot"
    ):
        bot_response = chatgpt_response(message=user_message)
        await message.channel.send(bot_response)
    await client.process_commands(message)
