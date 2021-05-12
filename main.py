# bot.py
import os
import re
import discord
import csv
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
        outputs = parseInput(input) # Fetches outputs from the user input using RegEx
        greeting += outputs[0] # Adds user note to printed output
        # TODO: Check if input date and time is valid (datetime in the future, not a past datetime)
        # TODO: Function to store parsed input
        #if time and date value is valid, then do # ? storeInput(outputs)
        storeInput(outputs)
        

        await message.channel.send(greeting)

# Parses the user input in the text channel
# * Returns: A default output string response from the bot.
def parseInput(input):
    output = ""
    dateMatch = re.search(r'\d{2}-\d{2}-\d{4}', input) #Isolates date
    timeMatch = re.search(r'\d{2}:\d{2}', input) #Isolates time

    # Isolates message
    noteMatch = input
    noteMatch = re.sub(r'\d{2}-\d{2}-\d{4}',"", noteMatch)
    noteMatch = re.sub(r'\d{2}:\d{2}:\d{2}',"", noteMatch)
    noteMatch = str(noteMatch.replace("/h",""))
    noteMatch = noteMatch.strip()

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
    # Match the note
    if noteMatch != None:
        output += " The message is: " + noteMatch

    outputs = [output, dateStr, timeStr, noteMatch] # Stores relevant outputs into a list
    return outputs

def storeInput(listOfInputs):
    with open("alerts.csv", mode='a+', newline="") as datawriter: #opens a CSV, will create if it doesn't exist
        datawriter = csv.writer(datawriter, delimiter=",")
        datawriter.writerow([listOfInputs[1],listOfInputs[2],listOfInputs[3],False])

client.run(TOKEN)

