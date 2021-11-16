import discord
from discord.ext import commands 
import os
import random
from webserver import keep_alive

client = commands.Bot(command_prefix = ">", case_insensitive=True)

Token = os.environ['Token']

@client.event
async def on_ready():
  print("We've logged in as {0.user}".format(client))

@client.event
async def on_member_join(member):
  member.channel.send(f"{member} has joined the server. Hope you enjoy your stay.")

@client.event
async def on_member_remove(member):
  member.channel.send(f"{member} has left the server.")

@client.event
async def on_message(message):
  if message.author == client.user:     # The bot user
    return
  
  greetings = ["hello","hi","hey","hey!","hi!","hello!"]

  responses = ["Hello there!","Hey, what's up?","How're you doing?","How are you?","Hi, what's the plan for today?"]
  
  if message.content.lower() in greetings:
    response = random.choice(responses)
    await message.channel.send(response)
  
  await client.process_commands(message)
  
@client.command()
async def say(ctx, *args):
  await ctx.message.delete()

  response = ''
  for word in args:
    response += ' ' + word

  await ctx.channel.send(response)

keep_alive()
client.run(Token)
