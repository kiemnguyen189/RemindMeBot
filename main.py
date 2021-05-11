# bot.py
import os
import re
import discord
from dotenv import load_dotenv
from datetime import datetime

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
    if input.lower().startswith('/h'):
        greeting += parseInput(input)   # ? Function to perform the RegEx
        # TODO: Function to store parsed input
        # TODO: Check if input date and time is valid (datetime in the future, not a past datetime)
        await message.channel.send(greeting)

# Parses the user input in the text channel
# * Returns: A default output string response from the bot.
def parseInput(input):
    output = ""
    dateMatch = re.search(r'\d{2}-\d{2}-\d{4}', input)
    timeMatch = re.search(r'\d{2}:\d{2}', input)
    # Match the date
    if dateMatch != None:
        date = datetime.strptime(dateMatch.group(), '%d-%m-%Y')
        dateStr = date.strftime('%d/%m/%Y')
        output += " The date is: " + dateStr
    # Match the time
    if timeMatch != None:
        time = datetime.strptime(timeMatch.group(), '%H:%M')
        timeStr = time.strftime('%H:%M')
        output += " The time is: " + timeStr
    # TODO: Store the user note
    return output

client.run(TOKEN)

