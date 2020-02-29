import discord
from discord.ext import commands
import requests

TOKEN = 'NjgzMjIyOTU0OTA5NDk5NDMw.XlobHQ.rAR8jMCu4Ma49m_WK3Boj14SLO0'

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    channels = ["feedback-text"]
    channels = ["bot-test"]

    if str(message.channel) in channels:

        if message.attachments:
            content = str(message.attachments)
            res = content.split()
            url = res[3]
            filename = res[2]
            name = filename[10:-5]

            ## This has to be changed in to linux env. since we host it in docker and make it lightweight
            
            link = r"C:\Users\bioni\Downloads\Xense" "\\" + str(name) + ".mp3"
            doc = requests.get(url[5:-3])
            open(link, 'wb').write(doc.content)

            channel = client.get_channel(682574846562926634)
            await channel.send(file=discord.File(link))

@client.command()
async def ping():
    await client.say("Pong!")


client.run(TOKEN)