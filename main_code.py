import discord
from discord.ext import commands 
import os
import random
from webserver import keep_alive

client = commands.Bot(command_prefix = ">", case_insensitive=True)

Token = os.environ['Token']



# Notifies when the bot comes online
@client.event
async def on_ready():
  print("{0.user} is ready.".format(client))

# Sends a message on member join
@client.event
async def on_member_join(member):
  member.channel.send(f"{member} has joined the server. Hope you enjoy your stay.")

# Sends a message on member leave
@client.event
async def on_member_remove(member):
  member.channel.send(f"{member} has left the server.")

# Replies to greetings with greetings
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



# Stops the bot from running
@client.command()
@commands.is_owner()
async def shutdown(ctx):
   await ctx.channel.send("Shut down successful.")
   await ctx.bot.logout()
  
# Repeats the message sent by the user
@client.command()
async def say(ctx, *args):
  await ctx.message.delete()

  response = ''
  for word in args:
    response += ' ' + word

  await ctx.channel.send(response)

# Evaluates a mathematical expression in a list
def evaluate(l):
    expression = ''
    for element in l:
        for sub_element in element:
            if sub_element == '×':
                sub_element = '*'
            if sub_element == '÷':
                sub_element = '/'
            elif sub_element == '^':
                sub_element = '**'
            elif sub_element == ' ':
                sub_element = ''
            expression += sub_element
    return eval(expression)

# Evaluates a mathematical expression entered by the user
@client.command(aliases = ['calc','solve','evaluate','eval'])
async def calculate(ctx, *args):
  try:
    await ctx.channel.send(evaluate(args))
  except ZeroDivisionError:
    await ctx.channel.send("ZeroDivisionError: Can't divide by 0.")

# Deletes a certain number of messages
@client.command(aliases = ['clear','delete'])
async def purge(ctx, amount=1):
  await ctx.channel.purge(limit = amount+1)

# Kicks a member
@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
  await member.kick(reason = reason)

# Bans a member
@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
  await member.ban(reason = reason)

# Unbans a MemoryError
@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
    
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"Unbanned user: {user.mention}")
      return

keep_alive()
client.run(Token)
