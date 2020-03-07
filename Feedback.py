import discord
from discord.ext import commands
from discord.ext import commands, tasks
import requests
import time
import asyncio
import csv
from discord.utils import get
from discord import NotFound
from itertools import cycle

client = commands.Bot(command_prefix='.')

TOKEN = 'NjgzMjIyOTU0OTA5NDk5NDMw.XlqomA.dyXMFHmJ6FkyPdlEr-y65QmhoGM'
DEV_TOKEN ='NjgzOTcwMTQxNzUwNTU4NzUz.XmODag.pgf4Hg_U4_FpSocLde9CUrCYAuk'

"""                
id's

"""

welcome_id = 409032133487755275
new_members_id = 685076937269706772
bot_test_id = 682921108172963841
bot_development_id = 682920811241537550
feedback_audio_id = 684123523337420876
vc_text_id = 492437954812313641
vc_id = 409121705827500034
producer_level_submission_id = 682610742863593473

new_member_role_id = 685030319446818821
producer_id = 409110516544438303
awaiting_submission_id = 685389934227750912
bot_developers_id = 682920532014137375

innovate_id = "202500280628150273"
stan_id = "685061943744004107"


"""                
Messages

"""

message_feedback = "It looks like you did not give feedback recently! :face_with_monocle:"
message_welcome = ",  welcome to **{Xense - Hardstyle Producers Group}** Please read #rules-and-info📃, give a confirmation in #new-members and have fun :tada::hugging: !"
message_confirmation = ", after confirmation please submit your best track in #producer-level-submission to get your producer level :slight_smile:. " \
                       "To access the server please confirm if you are a music producer by adding a reaction to this message with :thumbsup:, if not react with :thumbsdown:"
command_permission = "You don't have permission to use this command"
submission_await = "Reminder to submit your best track in #producer-level-submission to get your producer level  :medal:"

"""                
Timer

"""

author = set()
memes_enabled = False


async def log():
    await client.wait_until_ready()
    global author
    author = set()
    while not client.is_closed():
        try:
            author = set()
            await asyncio.sleep(3600)
        except Exception as e:
            await asyncio.sleep(3600)


async def no_feedback(client, message):
    if str(message.author.name) not in author:
        await message.channel.send(str(message.author.mention) + message_feedback)


"""                
Initialisation

"""


@client.event
async def on_ready():
    print('Bot is ready!')
    submission.start()
    await client.change_presence(activity=discord.Game(name='Stan is gey'))


"""                
on new member join

"""


@client.event
async def on_member_join(member):
    channel = client.get_channel(welcome_id)
    await channel.send("Hey " + str(member.mention) + message_welcome)
    role = get(member.guild.roles, id=int(new_member_role_id))
    await member.add_roles(role)
    channel = client.get_channel(new_members_id)
    await channel.send("Hey " + str(member.mention) + message_confirmation)


"""                
New member confirmation

"""


@client.event
async def on_raw_reaction_add(payload):
    if client.user.id != payload.user_id:
        channels = [new_members_id]
        if payload.channel_id in channels and "Admins" not in str(payload.member.roles): #str(payload.user_id) in adminID:
            channel = client.get_channel(new_members_id)
            if str(payload.emoji) == "👍":
                await channel.send("Accepted")
                member = payload.member
                new_member = get(member.guild.roles, id=int(new_member_role_id))
                await member.remove_roles(new_member)
                producer = get(member.guild.roles, id=int(awaiting_submission_id))
                await member.add_roles(producer)
                await channel.purge(limit=10 + 1)
            elif str(payload.emoji) == "👎":
                await channel.send("Denied")
            else:
                await channel.send("Invalid response")
        # else:
        #     print("correct")


"""                
Timer mention submission

"""

with open('timer.txt', newline='') as timer_file:
    last_time = float(timer_file.readlines()[0])


@tasks.loop(seconds=300)
async def submission():
    global last_time
    current_time = time.time()
    #print(last_time)
    #print(current_time)
    if current_time-last_time >= 172800:
        last_time = current_time
        notify = client.guilds[0].get_role(awaiting_submission_id)
        channel = client.get_channel(producer_level_submission_id)
        await channel.send(notify.mention + submission_await)
        with open('timer.txt', "w") as timer_write_file:
            timer_write_file.write(str(current_time))


"""                
.status - anyone

"""


@client.command()
async def status(ctx):
    if memes_enabled:
        meme_status = "enabled"
    else:
        meme_status = "disabled"
    await ctx.send("Bot is up and running!" + " Memes are " + meme_status)


"""                
.clear x - Stan

"""


@client.command()
async def clear(ctx, amount=1):
    if True in [(ID in str(ctx.author.id)) for ID in innovate_id]:
        await ctx.channel.purge(limit=amount+1)
    else:
        await ctx.channel.send(command_permission)


"""                
.meme_enable - admins
.meme_disable - admins

"""


@client.command()
async def memes_enable(ctx):
    if "Admins" in str(ctx.guild.get_member(ctx.author.id).roles):
        global memes_enabled
        memes_enabled = True
        await ctx.channel.send("Memes enabled")
    else:
        await ctx.channel.send(command_permission)


@client.command()
async def memes_disable(ctx):
    if "Admins" in str(ctx.guild.get_member(ctx.author.id).roles):
        global memes_enabled
        memes_enabled = False
        await ctx.channel.send("Memes disabled")
    else:
        await ctx.channel.send(command_permission)


"""                
.level

"""


@client.command()
async def level(ctx, name):
    if "Admins" in str(ctx.guild.get_member(ctx.author.id).roles):
        channel_id = producer_level_submission_id
        channel = client.get_channel(channel_id)
        found = False
        async for message in channel.history(limit=5000):
            log = str(message).lower()
            if str(name) in log:
                await ctx.send(name + " submitted")
                found = True
                break
        if not found:
            await ctx.send(name + " did not submit yet")
    else:
        await ctx.channel.send(command_permission)


"""                
On message

"""


@client.event
async def on_message(message):

    if client.user.id != message.author.id:

        """                
        Add memes

        """

        if message.content.startswith("!meme"):
            if "Admins" in str(message.author.roles):
                content = str(message.content)[6:]
                split = content.split(', ')
                if len(split) == 2:
                    words = open("words.txt", "a")
                    words.write(split[0] + "\n")
                    responses = open("responses.txt", "a")
                    responses.write(split[1] + "\n")
                    await message.channel.send("Meme added!")
            else:
                await message.channel.send(command_permission)

        """                
        Memes reply

        """

        if not message.content.startswith(".") and not message.content.startswith("!"):

            if memes_enabled is True:
                with open('words.txt', newline='') as input_file:
                    words = list(csv.reader(input_file))
                with open('responses.txt', newline='') as input_file:
                    responses = list(csv.reader(input_file))

                for i in range(len(words)):
                    if True in [(word.lower() in message.content.lower()) for word in words[i]]:
                        await message.channel.send(str(responses[i])[2:-2])

        """                
        Feedback  

        """

        channels = ["feedback"]

        if str(message.channel) in channels:

            global author

            """                
            Feedback audio 

            """

            if message.attachments:

                await no_feedback(client, message)
                attachment = message.attachments[0]
                link = r"C:\Users\Stanley\Downloads\Xense" "\\" + str(attachment.filename) + ".mp3"
                doc = requests.get(attachment.url)
                open(link, 'wb').write(doc.content)
                channel = client.get_channel(feedback_audio_id)
                await channel.send(str(message.author.mention), file=discord.File(link))

                """                
                Feedback links  
                          
                """

            elif "http" in message.content:
                if "youtube" in message.content or "clyp" in message.content or "dropbox" in message.content \
                        or "soundcloud" in message.content or "spotify" in message.content:
                    await no_feedback(client, message)
                    content = str(message.content)
                    split = content.split()
                    link = [i for i in split if i.startswith("http")]
                    channel = client.get_channel(feedback_audio_id)
                    await channel.send(str(message.author.mention) + " - " + str(link[0]))  # str(message.author)[:-5]

            else:
                author.add(str(message.author.name))
                print(author)

    await client.process_commands(message)


"""                
On voice chat connect

"""


# @client.event
# async def on_voice_state_update(member, before, after):
#     if before.channel == vc_id:
#         channel = client.get_channel(vc_text_id)
#         await channel.send("Who joined??")


client.loop.create_task(log())
client.run(DEV_TOKEN)