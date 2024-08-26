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
invincibleCounter = 0
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
    global invincibleCounter
    play = False
    botRole = discord.utils.get(message.guild.roles, id=859157866242113618)
    for word in message.content.lower().split():
        print(word)
        print(f"invincibleCounter = {invincibleCounter}")
        if (
            "invincible" in word
            or client.user.mentioned_in(message)
            or botRole in message.role_mentions
        ):
            play = True
            invincibleCounter += 1
    switch = {}
    for i in range(NUM_EPISODES):
        switch[i] = f"title_cards/Invincible{i+1}.mp4"
    if play:
        await message.channel.send(
            file=discord.File(
                switch.get((invincibleCounter - 1) % NUM_EPISODES, "No such file")
            )
        )
    await client.process_commands(message)


load_dotenv()

TOKEN = os.getenv("TOKEN")
print("TOKEN =", TOKEN)
client.run(TOKEN)
