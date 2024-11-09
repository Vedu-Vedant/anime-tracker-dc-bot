import discord
import os
from replit import db
from embeds import update_embed, helpEmbed, roleEmbed
from keep_alive import keep_alive
from discord.utils import get


client = discord.Client()


def get_text(anime_list):

  watched = ""
  for anime in anime_list[0]:
      watched += "{}\n".format(anime)
  
  watching = ""
  for anime in anime_list[1]:
      watching += "{}\n".format(anime)
  
  watchlist = ""
  for anime in anime_list[2]:
      watchlist += "{}\n".format(anime)

  return watched, watching, watchlist


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  users = db['users']

  # to check weather the user is our bot itself or not
  if message.author == client.user:
      return

  msg = message.content
  id = message.author.id
  username = "<@{}>".format(id)


  if username not in users.keys():
    db["users"][username] = [[], [], []]

  if msg.startswith("+"):
    command = msg.replace("+", "")
    
    watched = db['users'][username][0]
    watching = db['users'][username][1]
    watchlist = db['users'][username][2]
    

    if command.startswith("watchlist"):

      if command.startswith("watchlist remove "):
        anime = command.replace("watchlist remove ", "")
        anime_pos = watchlist.index(anime)
        del watchlist[anime_pos]
      
      elif command.startswith("watchlist bulk "):
        animes = command.replace("watchlist bulk ", "")

        if "," in animes:
          for anime in animes.split(", "):
            watchlist.append(anime)
        else:
          for anime in animes.split("\n"):
            watchlist.append(anime)

      else:
        anime = command.replace("watchlist ", "")
        watchlist.append(anime) 

      await message.channel.send(embed=update_embed(username))
    
    
    if command.startswith("watching"):

      if command.startswith("watching remove "):
        anime = command.replace("watching remove ", "")
        anime_pos = watching.index(anime)
        del watching[anime_pos]
      
      elif command.startswith("watching bulk "):
        animes = command.replace("watching bulk ", "")

        if "," in animes:
          for anime in animes.split(", "):
            watching.append(anime)
        else:
          for anime in animes.split("\n"):
            watching.append(anime)

      else:
        anime = command.replace("watching ", "")
        watching.append(anime)


      await message.channel.send(embed=update_embed(username))

    if command.startswith("watched"):

      if command.startswith("watched remove "):
        anime = command.replace("watched remove ", "")
        anime_pos = watched.index(anime)
        del watched[anime_pos]

        await message.channel.send(embed=update_embed(username))
      
      elif command.startswith("watched bulk"):
        animes = command.replace("watched bulk ", "")

        if "," in animes:
          for anime in animes.split(", "):
            watched.append(anime)
        else:
          for anime in animes.split("\n"):
            watched.append(anime)

        await message.channel.send(embed=update_embed(username))

      else:
        anime = command.replace("watched ", "")
        watched.append(anime)

        await message.channel.send(embed=update_embed(username)) 

    if command.startswith("list"):

      if len(command) > 4:
        user = command.replace("list ", "")

        if user in db['users']:
          watched, watching, watchlist = get_text(db['users'][user])
          watched_list = db['users'][user][0]

          if watched == "":
            watched = "None"
          
          if watching == "":
            watching = "None"
          
          if watchlist == "":
            watchlist = "None"
          
          if len(watched_list) > 50:
            con1Embed = discord.Embed(title = "Watchlist", description = "This is {} anime list\n{}".format(user, watchlist), colour=0x1aa3ff)
            con1Embed.add_field(name='Watching Anime', value=watching, inline=False)
            
            await message.channel.send(embed=con1Embed)

            con2Embed = discord.Embed(title = "Watched", description = watched, colour=0x1aa3ff)

            await message.channel.send(embed=con2Embed)

          
          myEmbed = discord.Embed(title = "Watchlist", description = "This is {} anime list\n{}".format(user, watchlist), colour=0x1aa3ff)
          myEmbed.add_field(name='Watching Anime', value=watching, inline=False)
          myEmbed.add_field(name='Watched Anime', value=watched, inline=False)
          await message.channel.send(embed=myEmbed)

        else:
          await message.channel.send("The users hasn't created a list")

      else:
        watched, watching, watchlist = get_text(db['users'][username])
        watched_list = db['users'][username][0]

        if watched == "":
          watched = "None"
        
        if watching == "":
          watching = "None"
        
        if watchlist == "":
          watchlist = "None"
        
        if len(watched_list) > 50:
          con1Embed = discord.Embed(title = "Watchlist", description = "{} this is your anime list\n{}".format(username, watchlist), colour=0x1aa3ff)
          con1Embed.add_field(name='Watching Anime', value=watching, inline=False)
          
          await message.channel.send(embed=con1Embed)

          con2Embed = discord.Embed(title = "Watched", description = watched, colour=0x1aa3ff)

          await message.channel.send(embed=con2Embed)
        
        myEmbed = discord.Embed(title = "Watchlist", description = "{} this is your anime list\n{}".format(username, watchlist), colour=0x1aa3ff)
        myEmbed.add_field(name='Watching Anime', value=watching, inline=False)
        myEmbed.add_field(name='Watched Anime', value=watched, inline=False)
        await message.channel.send(embed=myEmbed)
    
    if command.startswith("reset"):
      db["users"][username] = [[], [], []]

      myEmbed = discord.Embed(title = "Reset", description="Your anime list was reset", colour=0x1aa3ff)

      await message.channel.send(embed=myEmbed)
  
    if command.startswith("total"):

      if len(command) > 6:
        user = command.replace("total ", "")

        watched = db['users'][user][0]

        myEmbed = discord.Embed(title = "Watched Anime: {}".format(len(watched)), description="{} has watched {} animes\n\nRequested by {}".format(user, len(watched), username), colour=0x1aa3ff)

        await message.channel.send(embed=myEmbed)

      else:
        watched = db['users'][username][0]
        author = message.author

        myEmbed = discord.Embed(title = "{} has Watched Anime: {}".format(author, len(watched)), description="Requested by {}".format(username), colour=0x1aa3ff)

        await message.channel.send(embed=myEmbed)
    
    if command.startswith("help"):

      await message.channel.send(embed=helpEmbed)

    if command.startswith("roles"):

      await message.channel.send(embed=roleEmbed)



  watched = db['users'][username][0]
  num = len(watched)
  member = message.author
  
  if num >= 10:
    var = discord.utils.get(member.guild.roles, name = 'certified weeblet')
    
    await member.add_roles(var)
  
  if num >= 20:
    var = discord.utils.get(member.guild.roles, name = 'certified otaku')
    
    await member.add_roles(var)
  
  if num >= 30:
    var = discord.utils.get(member.guild.roles, name = 'certified weeb')
    
    await member.add_roles(var)
  
  if num >= 40:
    var = discord.utils.get(member.guild.roles, name = 'veteran weeb')
    
    await member.add_roles(var)
  
  if num >= 50:
    var = discord.utils.get(member.guild.roles, name = 'man of culture')
    
    await member.add_roles(var)
    


keep_alive()
client.run(os.getenv('TOKEN'))