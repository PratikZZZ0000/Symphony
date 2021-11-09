import discord 
import os
import random
from webserver import keep_alive


Token = os.environ['Token']

client = discord.Client()

@client.event
async def on_ready():
  print("We've logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:     # The bot user
    return
  
  introductions = ["hello","hi","hey","hey!","hi!","hello!"]

  responses = ["Hello there!","Hey, what's up?","How're you doing?","How are you?","Hi, what's the plan for today?"]
  
  if message.content.lower() in introductions:
    response = random.choice(responses)
    await message.channel.send(response)

  if message.content.startswith(">say"):
    await message.delete()
    words = message.content.split(' ')
    words.remove(">say")
    
    response = ""
    for word in words:
      response += f" {word}"

    await message.channel.send(response)

keep_alive()
client.run(Token)


