import db_tools
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import json
import os
import pafy
import requests
import shifumi as sh
import weather

load_dotenv()

DISCORD_TOKEN = os.getenv("discord_token")
RATP_URL = os.getenv("ratp_url")
RATP_CHANNEL = os.getenv("ratp_channel")
WEATHER_TOKEN = os.getenv("weather_token")

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

connection = db_tools.connection()

# Clear

@bot.command(name='clear', help='Clear all msg')
async def clear(ctx):
    await ctx.channel.purge()


# Hello

@bot.command(name='hello', help='Say hello')
async def hello(ctx):
    await ctx.channel.send('Hello {0.author.mention}'.format(ctx.message))

# History

@bot.listen()
async def on_command(ctx):
    db_tools.add_cmd(connection, str(ctx.message.content), str(ctx.message.author))


# Image
@bot.command(name='image', help='Random image')
async def image(ctx, length=200, height=300):
    request = requests.get("https://picsum.photos/" + str(length) + "/" + str(height))

    embed = discord.Embed()
    embed.set_image(url=request.url)

    return await ctx.channel.send(embed=embed)


# Météo

@bot.command(name='meteo', help='Display the weather')
async def meteo(ctx, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}&units=imperial'
    try:
        data = weather.parse_data(json.loads(requests.get(url).content)['main'])
        await ctx.channel.send(embed=weather.weather_message(data, city))
    except KeyError:
        await ctx.channel.send(embed=weather.error_message(city))


# Meven

@bot.command(name='meven', help='retard Méven')
async def meven(ctx):
    await ctx.channel.send('En effet Méven est en retard'.format(ctx.message))


# Ratp

@tasks.loop(seconds=900)  # 15 mins
async def ratp_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(RATP_CHANNEL))

    request = requests.get(RATP_URL)
    data = request.json()['result']

    alerts = {'metros': [], 'rers': [], 'tramways': []}

    for line in data['metros']:
        if not 'normal' in line['slug']:
            alerts['metros'].append(line)

    for line in data['rers']:
        if not 'normal' in line['slug']:
            alerts['rers'].append(line)

    for line in data['tramways']:
        if not 'normal' in line['slug']:
            alerts['tramways'].append(line)

    msg = ""

    if alerts['metros']:
        msg += "Métros:\n```"
        for line in alerts['metros']:
            msg += "Ligne " + line['line'] + " : " + line['title'] + "\n" + line['message'] + "\n"
        msg += "```"

    if alerts['rers']:
        msg += "\nRers:\n```"
        for line in alerts['rers']:
            msg += "Ligne " + line['line'] + " : " + line['title'] + "\n" + line['message'] + "\n"
        msg += "```"

    if alerts['tramways']:
        msg += "\nTramways:\n```"
        for line in alerts['tramways']:
            msg += "Ligne " + line['line'] + " : " + line['title'] + "\n" + line['message'] + "\n"
        msg += "```"

    if msg != "":
        await channel.send(msg)


ratp_task.start()


# Shifumi

@bot.command(name='shifumi', help='Play shifumi')
async def shifumi(ctx, shifumi_player='nothing'):
    await sh.play(ctx, shifumi_player)


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
        embed = discord.Embed(title="", description="I am currently not playing anything", color=discord.Color.red())
        return await ctx.send(embed=embed)
    elif vc.is_paused():
        return

    vc.pause()
    await ctx.send("Paused :pause_button:️")


@bot.command(name='resume', help='To resume song')
async def resume(ctx):
    vc = ctx.voice_client

    if not vc or not vc.is_connected():
        embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.red())
        return await ctx.send(embed=embed)
    elif not vc.is_paused():
        return

    vc.resume()
    await ctx.send("Resuming :play_pause:️")


@bot.command(name='stop', help='To stop song')
async def stop(ctx):
    vc = ctx.voice_client

    if not vc or not vc.is_connected():
        embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.red())
        return await ctx.send(embed=embed)

    vc.stop()
    await ctx.send("Stop :stop_button:️")


@bot.command(name='leave', help='Make leave the bot')
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("Bye ! :wave:️")
