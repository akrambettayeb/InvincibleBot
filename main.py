#!/usr/bin/env python3

from app.discord.discord import client, DISCORD_TOKEN

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
