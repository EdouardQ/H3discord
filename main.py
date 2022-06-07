import discord
import os
from dotenv import load_dotenv

class MyClient(discord.Client):
    input_channel = 983651129969770516
    ratp_channel = 983651171094921226
    music_channel = 983651061044764692

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello {0.author.mention}'.format(message))

load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token")

client = MyClient()
client.run(DISCORD_TOKEN)
