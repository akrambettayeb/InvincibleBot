#!/usr/bin/env python3

import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
import random
import itertools
from itertools import *
import json
import asyncio

def get_prefix(client, message):
    s = 'mark '
    prefixes = (
        list(map(''.join, itertools.product(*zip(s.upper(), s.lower())))))
    return commands.when_mentioned_or(*prefixes)(client, message)

status = cycle([discord.Game(name="Catch with Dad"),discord.Activity(type=discord.ActivityType.watching,name="INVINCIBLE")])

# File name for storing invincibleCounters
COUNTER_FILE = "invincibleCounters.json"

# Check if the file exists and read the value
if os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, 'r') as file:
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
    guild_id = str(message.guild.id)  # Convert to string for JSON serialization

    # Initialize the counter for the guild if it doesn't exist
    if guild_id not in invincibleCounters:
        invincibleCounters[guild_id] = 0

    play = False
    botRole = discord.utils.get(message.guild.roles, id=859157866242113618)
    for word in message.content.lower().split():
        print(word)
        if 'invincible' in word or client.user.mentioned_in(message) or botRole in message.role_mentions:
            play = True
            invincibleCounters[guild_id] += 1

    # Save the updated invincibleCounters to the file
    with open(COUNTER_FILE, 'w') as file:
        json.dump(invincibleCounters, file)

    switch = {
        0: 'title_cards/Invincible1.mp4',
        1: 'title_cards/Invincible2.mp4',
        2: 'title_cards/Invincible3.mp4',
        3: 'title_cards/Invincible4.mp4',
        4: 'title_cards/Invincible5.mp4',
        5: 'title_cards/Invincible6.mp4',
        6: 'title_cards/Invincible7.mp4',
        7: 'title_cards/Invincible8.mp4',
    }
    if play:
        await message.channel.send(file=discord.File(switch.get((invincibleCounters[guild_id] - 1) % 8, 'No such file')))
    await client.process_commands(message)

load_dotenv()

TOKEN = os.getenv("TOKEN")
print("TOKEN =", TOKEN)
client.run(TOKEN)
