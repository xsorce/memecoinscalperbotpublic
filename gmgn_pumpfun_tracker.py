import discord
from discord.ext import commands, tasks
import requests
from config import DISCORD_TOKEN, CHANNEL_ID, GMGN_API_URL, PUMPFUN_API_URL
from utils import format_token_alert, is_safe_token

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch_and_notify_tokens(source, url, channel):
    try:
        res = requests.get(url, timeout=5)
        tokens = res.json().get('data', []) if source == "gmgn" else res.json()

        for token in tokens[:10]:
            address = token.get("address") or token.get("tokenAddress") or ""
            if address and is_safe_token(address):
                alert = format_token_alert(token, source)
                await channel.send(alert)
    except Exception as e:
        print(f"{source.upper()} fetch error: {e}")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    trend_alerts.start()

@tasks.loop(minutes=5)
async def trend_alerts():
    channel = bot.get_channel(CHANNEL_ID)
    await fetch_and_notify_tokens("gmgn", GMGN_API_URL, channel)
    await fetch_and_notify_tokens("pumpfun", PUMPFUN_API_URL, channel)

bot.run(DISCORD_TOKEN)
