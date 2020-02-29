import discord
from discord.ext import commands
import requests

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    channels = ["feedback-text"]

    if str(message.channel) in channels:

        if message.attachments:
            content = str(message.attachments)
            res = content.split()
            url = res[3]
            filename = res[2]
            name = filename[10:-5]

            link = r"C:\Users\Stanley\Downloads\Xense" "\\" + str(name) + ".mp3"
            doc = requests.get(url[5:-3])
            open(link, 'wb').write(doc.content)

            channel = client.get_channel(682574846562926634)
            await channel.send(file=discord.File(link))

client.run('NjgzMjIyOTU0OTA5NDk5NDMw.XlobHQ.rAR8jMCu4Ma49m_WK3Boj14SLO0')