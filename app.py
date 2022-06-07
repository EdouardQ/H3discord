import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import pafy
import requests

load_dotenv()

DISCORD_TOKEN = os.getenv("discord_token")
RATP_URL = "https://api-ratp.pierre-grimaud.fr/v4/traffic"
RAPT_CHANNEL_ID = 983651171094921226

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


# Hello

@bot.command(name='hello', help='Say hello')
async def hello(ctx):
    await ctx.channel.send('Hello {0.author.mention}'.format(ctx.message))


# Ratp

@tasks.loop(seconds=900)#15 mins
async def ratp_task():
    request = requests.get(RATP_URL)
    data = request.json()['result']

    channel = bot.get_channel(RAPT_CHANNEL_ID)

    alerts = {'metros': [], 'rers': [], 'tramways': []}

    for line in data['metros']:
        if line['slug'] == 'normal': # A CHANGER POUR TEST
            alerts['metros'].append(line)

    for line in data['rers']:
        if line['slug'] == 'normal': # A CHANGER POUR TEST
            alerts['rers'].append(line)

    for line in data['tramways']:
        if line['slug'] == 'normal': # A CHANGER POUR TEST
            alerts['tramways'].append(line)

    if alerts['metros']:
        for line in alerts['metros']:
            msg = "Ligne : " + line['line'] + " - " + line['title'] + "\n" + line['message']
            # await channel.send(msg)   #buged



ratp_task.start()

# Youtube

@bot.command(name='play', help='To play song')
async def play(ctx, url):
    vc = ctx.voice_client

    if not vc or not vc.is_connected:
        channel = ctx.author.voice.channel
        await channel.connect()

    # re fetch voice_client
    if vc is None:
        vc = ctx.voice_client

    if vc.is_playing() or vc.is_paused():
        vc.stop()

    video = pafy.new(url)
    best = video.getbestaudio()

    source = discord.FFmpegPCMAudio(best.url, executable="ffmpeg")

    vc.play(source, after=None)
    await ctx.send("Playing " + str(best.title) + " :arrow_forward:️")


@bot.command(name='pause', help='To pause song')
async def pause_(ctx):
    vc = ctx.voice_client

    if not vc or not vc.is_playing():
        embed = discord.Embed(title="", description="I am currently not playing anything", color=discord.Color.green())
        return await ctx.send(embed=embed)
    elif vc.is_paused():
        return

    vc.pause()
    await ctx.send("Paused :pause_button:️")


@bot.command(name='resume', help='To resume song')
async def resume(ctx):
    vc = ctx.voice_client

    if not vc or not vc.is_connected():
        embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
        return await ctx.send(embed=embed)
    elif not vc.is_paused():
        return

    vc.resume()
    await ctx.send("Resuming :play_pause:️")


@bot.command(name='stop', help='To stop song')
async def stop(ctx):
    vc = ctx.voice_client

    if not vc or not vc.is_connected():
        embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
        return await ctx.send(embed=embed)

    vc.stop()
    await ctx.send("Stop :stop_button:️")


@bot.command(name='leave', help='Make leave the bot')
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("Bye ! :wave:️")
