import datetime, re
import copy
import logging
import traceback
import aiohttp
import sys
from collections import Counter, deque
import discord
from discord.ext import commands
import requests
from discord import client

# client = commands.Bot(command_prefix = '.')

# @client.event
# async def on_ready():
#     print('Bot is ready!')

# @client.event
# async def on_message(message):
#     # channels = ["feedback-text"]
#     channels = ["bot-test"]

#     if str(message.channel) in channels:

#         if message.attachments:
#             content = str(message.attachments)
#             res = content.split()
#             url = res[3]
#             filename = res[2]
#             name = filename[10:-5]

#             ## This has to be changed in to linux env. since we host it in docker and make it lightweight

#             link = r"C:\Users\bioni\Downloads\Xense" "\\" + str(name) + ".mp3"
#             doc = requests.get(url[5:-3])
#             open(link, 'wb').write(doc.content)
            
#             #bot-test channel
#             channel = client.get_channel(682921108172963841)
#             await channel.send(text='Ping!')

#             # #feedback-channel
#             # channel = client.get_channel(682574846562926634)
#             # await channel.send(file=discord.File(link))

# @client.command()
# async def ping():
#     await client.say("Pong!")

# @client.command()
# async def echo(*args):
#     output = ''
#     for word in args:
#         output += word
#         output += ' '
#     await client.say(output)

# client.run(TOKEN)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    if online:
        await client.change_presence(activity=discord.Game(name="Command prefix: " + compref))
    else:
        await client.change_presence(status=discord.Status("offline"))

@client.event
async def on_message(message):
    print ('User has sent a message')
        
    
@client.command()
async def ping(ctx):
    await ctx.send(f'pong {round(client.latency * 100)} ms')

# @client.command()
# async def echo(*args):
#     output = 'pong!'
#     for word in args:
#         output += word
#         output += ' '
#     await client.say(output)
    
token = 'NjgzMjIyOTU0OTA5NDk5NDMw.XlqVNA.tJfe_3QMFhpdSfZDZqqxS1OZnFs'
client.run(token)