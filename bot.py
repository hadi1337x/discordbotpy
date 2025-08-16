# bot.py
import os, requests
import discord
from discord import Intents

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
SOURCE_CHANNEL_ID = int(os.environ["https://discordapp.com/channels/1187388943776362637/1257895754140352562"])
DEST_WEBHOOK_URL = os.environ["https://discordapp.com/api/webhooks/1406410280166101123/deKqoMLnb2HyBqkCVvahf21mAtd3bDlXGwi_94q4Wvb1pz3KedPgm5KHcV-eluQSAwuM"]

intents = Intents.default()
intents.message_content = True

class Relay(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, m: discord.Message):
        if m.author.bot or m.channel.id != SOURCE_CHANNEL_ID:
            return
        content = m.content or ""
        if m.attachments:
            content += ("\n" if content else "") + "\n".join(a.url for a in m.attachments)
        payload = {
            "username": m.author.display_name,
            "avatar_url": m.author.display_avatar.url if m.author.display_avatar else None,
            "content": content[:2000] or " "
        }
        r = requests.post(DEST_WEBHOOK_URL, json=payload, timeout=10)
        r.raise_for_status()

client = Relay(intents=intents)
client.run(TOKEN)
