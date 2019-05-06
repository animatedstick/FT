import discord
import asyncio
import requests
import os
from discord.ext import commands


BOT_TOKEN = os.getenv("BOT_TOKEN")
FORTNITE_API_TOKEN = os.getenv("FT_TOKEN")
COMMAND_PREFIX = 'c!' , 'C!' ,'charlie ','c' , '<@568492275504775178> ' , 'C'

client = discord.Client()
prefix = 'f!' 
client = commands.Bot(command_prefix=prefix, description='A Discord Bot By the AnimatedStick#4797')

@client.event
async def on_ready():
  #await client.change_presence(activity=discord.Game(name='Type #help'))
  print("Done")

@client.event
async def on_message(message):
  if message.content.startswith(COMMAND_PREFIX + 'ft'):
    words = message.content.split(' ', 2)

    if len(words) < 3:
      await message.channel.send('Usage: `c!stats <pc,xbl,psn> <nickname>`')
      return

    platform = words[1].lower()

    # more acceptable platform names
    if platform == 'xbox':
      platform = 'xbl'
    elif platform == 'ps4':
      platform = 'psn'

    if platform not in ('pc','xbl','psn'):
      await message.channel.send('Usage: `c!stats <pc,xbl,psn> <nickname>`')
      return
    else:
      res = fortnite_tracker_api(platform,words[2])

      if res:
        matches_played = res[0]['value']
        wins = res[1]['value']
        win_percent = res[2]['value']
        kills = res[3]['value']
        kd = res[4]['value']


        embed=discord.Embed(title="Fortnite Stats", url="https://www.epicgames.com/fortnite/buy-now", color=0x8000ff)
        embed.set_author(name=words[2], icon_url="https://cdn.discordapp.com/attachments/567025926756499458/575005939015352351/Fortnite_large.jpg")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/567025926756499458/575005939015352351/Fortnite_large.jpg")
        embed.add_field(name="Name", value=words[2], inline=True)
        embed.add_field(name="Matches Played", value="{}".format(matches_played), inline=True)
        embed.add_field(name="Wins", value="{}".format(wins), inline=True)
        embed.add_field(name="Win Percentage", value=win_percent, inline=True)
        embed.add_field(name="Kills", value="{}".format(kills), inline=True)   
        embed.add_field(name="K/D", value=kd, inline=True)
        embed.set_footer(text=f"Fortnite Stats For {words[2]}",icon_url=str(message.author.avatar_url))
        await message.channel.send( embed=embed)
      else:
        await message.channel.send( 'Failed to get data. Double check spelling of your nickname.')

def fortnite_tracker_api(platform, nickname):
  URL = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + nickname
  req = requests.get(URL, headers={"TRN-Api-Key": FORTNITE_API_TOKEN})

  if req.status_code == 200:
    try:
      #print(req.json())
      lifetime_stats = req.json()['lifeTimeStats']
      return lifetime_stats[7:]
    except KeyError:
      return False
  else:
    return False

client.run(BOT_TOKEN)
