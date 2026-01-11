# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import logging
import threading

from dotenv import load_dotenv
import os
import connexion

load_dotenv()
token = None

# Write logs to a file under `logs/` (created in the image) so they are
# persisted inside the container filesystem and owned by the runtime user.
#handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='a')
# Configure logging via the standard library instead of passing handlers
# into `bot.run()`, which forwards to `Client.start()` and does not
# accept `log_handler`/`log_level` keyword args.
#logging.basicConfig(level=logging.DEBUG, handlers=[handler])
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot=commands.Bot(command_prefix = 'b!', intents = intents)

@bot.event
async def on_ready():
    print(f"start of bot")

@bot.event
async def on_message(message):
    print(f"processing")
    if message.author == bot.user:
        return
    if "sibal" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} no slurs")
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}")


def run_api():
    """Run the Connexion API server in a separate thread"""
    try:
        import api
        api.set_bot(bot)
        
        app = connexion.App(__name__, specification_dir='./')
        app.add_api('openapi.yaml')
        
        print("Starting API server on http://0.0.0.0:8080")
        # Run on port 8080
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"Error starting API server: {e}")
        import traceback
        traceback.print_exc()


# Start the API server in a background thread
api_thread = threading.Thread(target=run_api, daemon=False)
api_thread.start()

# Run the Discord bot
print("Starting Discord bot...")
bot.run(token)