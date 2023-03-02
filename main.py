import discord
import os
import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from Tools.utils import getGuildPrefix
from Tools.translate import Translate
#from .archive.instagram import main_instagram
#import warnings

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(getGuildPrefix, intents = intents)

# HELP
bot.remove_command("help") # To create a personal help command 

# Translate
bot.translate = Translate()

# Filter
#warnings.filterwarnings(
#    "ignore",
#    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
#)

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')
    print(discord.__version__)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"the Village"))

# ------------------------ RUN ------------------------ # 
with open("config.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    
    #scheduler = AsyncIOScheduler()

    #scheduler.add_job(main_instagram, CronTrigger(second="10"))

    #scheduler.add_job(main_spotify, CronTrigger(second="10"))

    #scheduler.start()
bot.run(token) 