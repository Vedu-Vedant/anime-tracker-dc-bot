import discord

helpEmbed = discord.Embed(title = "General instructions", description="The prefix for this bot is '+'\nuse total to get total animes watched\nuse reset to reset your entire list\nUser +roles to get info on roles", colour=0x1aa3ff)
helpEmbed.add_field(name="Adding anime", value = "+list anime\nfor eg +watchlist naruto\nTo add animes in bulk use this +watched bulk anime1, anime2, etc", inline=False)
helpEmbed.add_field(name="Removing anime", value = "+list remove anime\nfor eg +watchlist remove naruto", inline=False)



roleEmbed = discord.Embed(title = "Roles", description="You will get these roles based on how much animes you have watched:-\n\n10+ animes watched = certified weeblet\n20+ animes watched = certified otaku\n30+ animes watched = certified weeb\n40+ animes watched = veteran weeb\n50+ animes watched = man of culture", colour=0x1aa3ff)

def update_embed(username):
  updateEmbed = discord.Embed(title = "Updated", description="Requested by {}".format(username), colour=0x1aa3ff)

  return updateEmbed