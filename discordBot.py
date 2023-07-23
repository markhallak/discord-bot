import os

import discord
from discord.ext import commands, tasks
import asyncio

from nomiAI import NomiAI

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Your bot is ready")

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == "Testing":
            break


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '99!':
        await message.channel.send("99!")
    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_error(event, *args):
    if event == 'on_message':
        print(f'Unhandled message: {args[0]}\n')


@bot.command(name='start')
async def nine_nine(ctx):
    await ctx.send("Please answer the following questions first so we can create a suitable personality for you.")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    questions = ["What is your name?",
                 "Please select your AI companion's preferred gender: (Type the number for the respective chosen gender e.g. 1)\n\n"
                 "1: Male   2: Female   3: Nonbinary",
                 "What do you wish to name your AI Companion?",
                 ]

    name = ""
    gender = ""
    aiName = ""

    try:
        # Listen for the next 3 messages from the same user in the same channel
        for j in range(3):
            await ctx.send(questions[j])
            response = await bot.wait_for('message', check=check, timeout=120.0)

            if j == 0:
                name = response.content
            elif j == 1:
                gender = response.content
            else:
                aiName = response.content


    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. If you wish to start over, use the !start command.")

    await ctx.send("Please wait...")

    try:
        await NomiAI().run(name, gender, aiName, ctx, bot)
    except Exception as e:
        print(e)


async def initClient():
    print("Client starting to run...")
    await client.start(os.environ['TOKEN_SECRET'])


async def initBot():
    print("Bot starting to run")
    await bot.start(os.environ['TOKEN_SECRET'])


async def main():
    tasks = [initClient(), initBot()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()