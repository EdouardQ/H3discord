import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pafy

load_dotenv()

DISCORD_TOKEN = os.getenv("discord_token")

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name='play', help='To play song')
async def play(ctx, url):
    channel = ctx.author.voice.channel
    await channel.connect()

    video = pafy.new(url)
    best = video.getbest()

    source = discord.FFmpegPCMAudio(best.url, executable="ffmpeg")
    ctx.voice_client.play(source, after=None)


@bot.command(name='leave', help='Make leave the bot')
async def leave(ctx):
    await ctx.voice_client.disconnect()
