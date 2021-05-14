# bot.py
import csv
import os
import re
from datetime import datetime

import discord
from discord.ext import tasks
from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

global superHost, superUser, superPassword

superHost = "localhost"
superUser = "root"
superPassword = "MySQL123"



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
    await fetch_notes.start()

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

# Fetches the notes from the database and prints any one who's conditions are met
# * Returns: A reminder for the note when the time is right
@tasks.loop(seconds=10) # task runs every x seconds
async def fetch_notes():
    channel = client.get_channel(841088520927182901) #channel ID
    try: #creates connection with local MySQL server
        with connect(
            host= superHost,
            user= superUser,
            password = superPassword,
            database= "alerts"
        ) as connection:
            queryToWrite = "SELECT * FROM alerts.alert_store WHERE sent = 0 ORDER BY dates asc, times asc;" #selects only unsent messages from table, sorted by date and time so earliest first
            with connection.cursor() as cursor:
                cursor.execute(queryToWrite)
                result = cursor.fetchall() #fetches all the data
                for row in result: #iterate through the results
                    list(row) #casts the data as a list

                    #manipulates the time and date into a datetime format
                    comapreDatetime = str(row[1]) + " " + str(row[2])
                    comapreDatetime = datetime.strptime(comapreDatetime, "%Y-%m-%d %H:%M:%S")

                    #gets current datetime
                    currentDatetime = datetime.now()

                    #if the current time is equal or 'later' than the comparator, send a message to the channel
                    if (currentDatetime >= comapreDatetime) and row[-1] == 0:
                        reminderString = "Reminder: " + row[-2]
                        await channel.send(reminderString)
                        update_notes(row[0]) #updates the data in the table by using the primary key which is 'id'
    except Error as e:
        print(e)    

    #await channel.send(row)

#if a note's datetime is valid and hasn't bee
# * Returns: Nothing 
def update_notes(toDel):
    try:
        with connect(
            host= superHost,
            user= superUser,
            password = superPassword,
            database= "alerts"
        ) as connection:

            queryToWrite = "UPDATE alerts.alert_store SET sent = True WHERE id ='" + str(toDel) + "';"
            with connection.cursor() as cursor:
                cursor.execute(queryToWrite)
                connection.commit() #commiting query. Required.

    except Error as e:
        print(e)        

# Parses the user input in the text channel
# Returns: A list containing:
# * Text output
# * Date string
# * Time string
# * User note
def parseInput(input):
    output = ""
    dateMatch = re.search(r'\d{2}-\d{2}-\d{4}', input) #Isolates date
    timeMatch = re.search(r'\d{2}:\d{2}', input) #Isolates time

    # Isolates message
    noteMatch = input
    noteMatch = re.sub(r'\d{2}-\d{2}-\d{4}',"", noteMatch)
    noteMatch = re.sub(r'\d{2}:\d{2}',"", noteMatch)
    noteMatch = str(noteMatch.replace("/h",""))
    noteMatch = noteMatch.strip()
    if noteMatch.startswith(":"):
        noteMatch = noteMatch[3:]
    noteMatch = noteMatch.strip()

    # Match the date
    if dateMatch != None:
        date = datetime.strptime(dateMatch.group(), '%d-%m-%Y')
        dateStr = date.strftime('%d/%m/%Y')
        output += " An alert is set for " + dateStr
        dateStr = date.strftime('%Y:%m:%d')
    # Match the time
    if timeMatch != None:
        time = datetime.strptime(timeMatch.group(), '%H:%M')
        timeStr = time.strftime('%H:%M')
        output += " at " + timeStr
    # TODO: Store the user note
    # Match the note
    if noteMatch != None:
        output += ". The message is: " + noteMatch

    outputs = [output, dateStr, timeStr, noteMatch] # Stores relevant outputs into a list
    return outputs

#stores the user input into the mysql table
def storeInput(listOfInputs):
    try: #creates connection with local MySQL server
        with connect( 
            host= superHost,
            user= superUser,
            password = superPassword,
            database= "alerts"
        ) as connection: #formulates a query to write to the database 
            queryToWrite = "INSERT INTO `alert_store` (dates, times, note, sent) VALUES ('" + listOfInputs[1] + "','" + listOfInputs[2] + "','" + listOfInputs[3] + "',False);" #forming query
            with connection.cursor() as cursor:
                cursor.execute(queryToWrite)
                connection.commit() #commiting query. Required.
    except Error as e:
        print(e)

client.run(TOKEN)

