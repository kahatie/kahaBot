import discord
import os
import requests
import json

client = discord.Client()

ethermine_api = "https://api.ethermine.org"

#help msg
def get_help_msg():
  embed=discord.Embed(title="help", color=0x355271)
  embed.add_field(name='k!help', value="ce message", inline=False)
  embed.add_field(name='k!hello', value="bot say hello", inline=False)
  embed.add_field(name='k!stat', value="ethermine stat", inline=False)
  return(embed)

#return new discord embed with ethermine decorator
def create_ethermine_embed(title=""):
  embed=discord.Embed(title=title, color=0x8000ff)
  embed.set_author(name='Ethermine Stats', icon_url='https://play-lh.googleusercontent.com/19x69QGQUQrSxROHruKZ-Gl55664xv5Q_nHOHLCsLZ_EPXhQ6VLL9kWXGNc_ukJ4Y-k=s180')
  return(embed)

#check eth adress is valid
def ethIdIsValid(id=""):
  return(42 == len(str(id)))

#ethermine pool stat 
def get_ethermine_stat():
  response = requests.get(ethermine_api + "/poolStats")
  json_data = json.loads(response.text)
  hashRate = json_data['data']['poolStats']['hashRate']
  activeMiners = json_data['data']['poolStats']['miners']
  workers = json_data['data']['poolStats']['workers']
  blocksPerHour = json_data['data']['poolStats']['blocksPerHour']
  price_usd = json_data['data']['price']['usd']

  embed=create_ethermine_embed()
  embed.add_field(name='Hashrate', value=str(round(hashRate / 1000000000000 , 1)) + 'TH/s', inline=False)
  embed.add_field(name='Active Miners', value=str(activeMiners), inline=False)
  embed.add_field(name='Workers', value=str(workers), inline=False)
  embed.add_field(name='Blocks/h', value=str(blocksPerHour), inline=False)
  embed.add_field(name='Price', value=str(price_usd) + '$', inline=False)

  return(embed)
# ethermine miner stat
def get_ethermine_minerstat(minerId=""):

  #check minerId 
  if not ethIdIsValid(minerId):
    embed=create_ethermine_embed()
    embed.add_field(name='Invalide Id', value= str(minerId), inline=True)
    return(embed)

  response = requests.get(ethermine_api + '/miner/{}/currentStats'.format(minerId))
  json_data = json.loads(response.text)
  
  report_hash = json_data['data']['reportedHashrate']
  current_hash = json_data['data']['currentHashrate']
  average_hash = json_data['data']['averageHashrate']
  usdPerMin = json_data['data']['usdPerMin']
  valid_shares = json_data['data']['validShares']
  invalid_shares = json_data['data']['invalidShares']
  stale_shares = json_data['data']['staleShares']
  active_workers = json_data['data']['activeWorkers']


  embed=create_ethermine_embed()
  embed.add_field(name='Reported Hashrate', value=str(report_hash / 1000000 )[0:-5] + ' MH/s', inline=False)
  embed.add_field(name='Actual Hashrate', value= str(current_hash / 1000000 )[0:-13] + ' MH/s', inline=False)
  embed.add_field(name='Average Hashrate', value=str(average_hash / 1000000 )[0:-13] + ' MH/s', inline=False)
  embed.add_field(name='USD per Month', value=str(usdPerMin * 60 * 24 * 30.4167 )[0:-14] + ' $', inline=False)
  embed.add_field(name='Valid Shares', value=valid_shares, inline=False)
  embed.add_field(name='Invalid Shares', value=invalid_shares, inline=False)
  embed.add_field(name='Stale Shares', value=stale_shares, inline=False)
  embed.add_field(name='Active Workers', value=active_workers, inline=False)
  embed.set_footer(text="KahaBot")
  return(embed)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('k!hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('k!help'):
        await message.channel.send(embed=get_help_msg())
    if message.content.startswith('k!stat'):
        await message.channel.send(embed=get_ethermine_stat())
    if message.content.startswith('k!minerstat'):
        minnerId = message.content.split('k!minerstat ',1)[1]
        await message.channel.send(embed=get_ethermine_minerstat(minnerId))

client.run(os.getenv('TOKEN'))
