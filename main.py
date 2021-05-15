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
    userID = message.author.id
    if input.lower().startswith('/h'):
        outputs = parseInput(input,userID) # Fetches outputs from the user input using RegEx
        try:
            greeting += outputs[0] # Adds user note to printed output
            # TODO: Check if input date and time is valid (datetime in the future, not a past datetime)
            # TODO: Function to store parsed input
            #if time and date value is valid, then do # ? storeInput(outputs)
            storeInput(outputs)
            await message.channel.send(greeting)
        except:
            print("Input Error")


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
            queryToWrite = "SELECT * FROM alerts.alert_store WHERE sent = 0 ORDER BY date_notify asc, time_notify asc;" #selects only unsent messages from table, sorted by date and time so earliest first
            with connection.cursor() as cursor:
                cursor.execute(queryToWrite)
                result = cursor.fetchall() #fetches all the data
                for row in result: #iterate through the results
                    list(row) #casts the data as a list

                    #manipulates the time and date into a datetime format
                    compareDatetime = str(row[1]) + " " + str(row[2])
                    compareDatetime = datetime.strptime(compareDatetime, "%Y-%m-%d %H:%M:%S")

                    #gets current datetime
                    currentDatetime = datetime.now()
                    #print(currentDatetime >= compareDatetime, currentDatetime, compareDatetime)

                    #if the current time is equal or 'later' than the comparator, send a message to the channel
                    if (currentDatetime >= compareDatetime) and row[-1] == 0:
                        reminderString = " <@" + str(row[-4]) + "> " + row[-2]
                        print(reminderString)
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
def parseInput(input, userID):
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
    noteMatch = noteMatch.replace("'","\\'")
    noteMatch = noteMatch.replace('"','\\"')

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
    if (dateMatch != None) and (timeMatch != None):
        delta =  datetime.combine(date.date(), time.time()) - datetime.now()
        dateNow = date.now()
        timeNow = time.now()
    # Match the note
    if noteMatch != None:
        output += ". The message is: " + noteMatch

    if not str(delta).startswith("-"):
        outputs = [output, dateStr, timeStr, dateNow, timeNow, userID, delta, noteMatch] # Stores relevant outputs into a list
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
            queryToWrite = "INSERT INTO `alert_store` (date_notify, time_notify, date_created, time_created, userID, delta, note, sent) VALUES ('" + listOfInputs[1] + "','" + listOfInputs[2] + "','" + str(listOfInputs[3]) + "','" + str(listOfInputs[4]) +  "','" + str(listOfInputs[5]) + "','" + str(listOfInputs[6]) + "','" + listOfInputs[7] + "',False);"  #forming query
            with connection.cursor() as cursor:
                cursor.execute(queryToWrite)
                connection.commit() #commiting query. Required.
    except Error as e:
        print(e)

client.run(TOKEN)  

