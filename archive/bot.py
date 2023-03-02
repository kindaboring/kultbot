# bot.py
import os
import time
import discord
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from instagram import *
from spotify import *
from discord.ext import commands
from dotenv import load_dotenv
import warnings

load_dotenv()

warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)

TOKEN = os.getenv('DISCORD_TOKEN') # bot token from .env file

client = commands.Bot(command_prefix='!') # each command is called through this prefix

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Kult Village!') # discord bot connection verification

    scheduler = AsyncIOScheduler()

    scheduler.add_job(main_instagram, CronTrigger(second="10"))

    #scheduler.add_job(main_spotify, CronTrigger(second="10"))

    scheduler.start()

client.run(TOKEN)