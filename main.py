import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()
token = os.environ['token']

trigger_words = ["sad", "unhappy", "angry", "shit"]
starter_messages = ["Heads up", "Everything gone be alright", "After the rain comes the sunshine"]

def update_reactions(reaction_msg):
  if "reactions" in db.keys():
    reactions = db["reactions"]
    reactions.append(reaction_msg)
    db["reactions"] = reactions
  else:
    reactions = starter_messages
    reactions.append(reaction_msg)
    db["reactions"] = reactions

def delete_reactions(ind):
  reactions = db["reactions"]
  if len(reactions) > ind:
    del reactions[ind]
    db["reactions"] = reactions
    
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - [" +json_data[0]['a'] +"]"
  return quote
  
@client.event
async def onready():
  print('We have logged in as {0.user}',format(client))

@client.event
async def on_message(message):
  msg = message.content
  
  if message.author == client.user:
    return

  if msg.startswith('inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_messages
  if "reactions" in db.keys():
    options = db["reactions"]
    
  if any(word in msg for word in trigger_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$add"):
    reaction_msg = msg.split("$add ", 1)[1]
    update_reactions(reaction_msg)
    await message.channel.send("New reaction added")

  if msg.startswith("$list"):
    await message.channel.send(db["reactions"])

  if msg.startswith("$del"):
    reactions = []
    if "reactions" in db.keys():
      ind = int(msg.split("$del ", 1)[1])
      delete_reactions(ind)
      reactions = db["reactions"]
    await message.channel.send(reactions)

keep_alive()
client.run(token)

