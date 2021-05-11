# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} has connected to: '
        f'{guild.name} (id: {guild.id}) '
        f'{client.user} kappa1234'
    )

@client.event
async def on_message(message):
    # * Ignore messages sent by itself.
    if message.author == client.user:
        return
    greeting = "Hi!"
    input = message.content
    # if "hello" in input.lower():
    #     response = greeting
    #     await message.channel.send(response)
    # TODO: RegEx for inputs.
    if input.lower().startswith('.h'):
        await message.channel.send(greeting)


client.run(TOKEN)

