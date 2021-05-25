import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

pp_words = ["pp", "PP", "peanus", "dick", "penis"]
sad_words = ["sad", "depressed", "bully", ":("]

pp_response = "Your pp = 8=D, My pp is 8========D. Get gud."
starter_encouragements = [
  "Cheer up, It'll get larger.",
  "Hang in there, It'll get larger.",
  "Don't worry, you are still a great person! It'll get larger."
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('-quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("-new"):
    encouraging_message = msg.split("-new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("-del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("-del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("-list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("-responding"):
    value = msg.split("-responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

  if any(word in msg for word in pp_words):
      await message.channel.send(pp_response)

  if msg.startswith('-help'):
    await message.channel.send("""
    Hello! Thank you for inviting me to your server, my prefix is [-]
    These are the commands that are currently available. More will be added in the future:

    -quote - Generates a random quote from an api database
    -new - Creates a new encouraging message
    -del - Deletes an encouraging message
    -list - Generates a list of encouraging messages in the database currently
    -responding true/false - Enables and Disable the feature to respond with an encouragaing message
    """)
  
keep_alive()
client.run(os.environ['TOKEN'])