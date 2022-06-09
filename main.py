from discord.ext import commands
import discord.embeds
from googlesearch import search
from baidusearch.baidusearch import search as bsearch
import os
import bs4
import requests

prefix = '!'
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,activity=discord.Activity(name=prefix, type=discord.ActivityType.listening))

@bot.command()
async def hello(ctx):
  await ctx.send('Hello, ' + ctx.author.display_name + "!")

@bot.command()
async def bing(ctx,req:str):
  embed = discord.Embed(title = 'Google Search for ' + req)
  query = req

  url = 'https://www.bing.com/search?q=' + query
  print(url)
  
  requests_results = requests.get(url)
  
  soup_link = bs4.BeautifulSoup(requests_results.content, "html.parser")
  links = soup_link.find_all("h2")
  for link in links:
    pagetitle = link.text
    pagelink = link.find('a')['href'] 
    embed.add_field(name = pagetitle, value = pagelink, inline = False)
    embed.set_thumbnail(url='https://banner2.cleanpng.com/20180714/zks/kisspng-bing-news-logo-microsoft-msn-hoodie-twitch-5b49d27f3a4c55.7426910315315646712388.jpg')
  embed.set_footer(text = 'This search was done by Search Bot')
  await ctx.send(embed = embed)

@bot.command()
async def baidu(ctx, req:str, num = None):
  if num is None:
    num = 1
  num = int(num)
  if num < 1:
    num = 1
  embed = discord.Embed(title = 'Baidu Search for ' + req)
  start = (num-1)*10
  counter = 0
  reslist = bsearch(req, num_results = num*10)
  print(reslist)
  for url in reslist:
    if(counter > start):
      embed.add_field(name = url['title'], value = url['url'], inline = False)
    counter = counter + 1
  embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJA_c8ZqNPZyhBbjHL37NwVFlbS-iINKc_Lw&usqp=CAU')
  embed.set_footer(text = 'This search was done by Search Bot')
  await ctx.send(embed = embed)

@bot.command()
async def google(ctx,req:str,num = None):
  if num is None:
    num = 1
  num = int(num)
  if num < 1:
    num = 1
  embed = discord.Embed(title = 'Google Search for ' + req)
  url = 'https://google.com/search?q=' + req + "&start=" + str((num - 1) * 10)
  requests_results = requests.get(url)
  soup_link = bs4.BeautifulSoup(requests_results.content,   "html.parser")
  links = soup_link.find_all("a")

  for link in links:
    link_href = link.get('href')
    if "url?q=" in link_href and not "webcache" in link_href:
      title = link.find_all('h3')
      if len(title) > 0:
          pagelink = link.get('href').split("?q=")[1].split("&sa=U")[0]
          pagetitle = title[0].getText()
          embed.add_field(name = pagetitle, value = pagelink, inline = False)
  embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png')
  embed.set_footer(text = 'This search was done by Search Bot')
  await ctx.send(embed = embed)

@bot.command()
async def google2(ctx,req:str,num = None):
  if num is None:
    num = 1
  num = int(num)
  if num < 1:
    num = 1
  embed = discord.Embed(title = 'Google Search for ' + req)
  start = (num-1)*10
  counter = 0
  reslist =  search(req, num_results = num*10,lang ='en', advanced = True)
  print(reslist)
  for url in reslist:
    if(counter > start):
      embed.add_field(name = url.title, value = url.url, inline = False)
    counter = counter + 1
    
  embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png')
  embed.set_footer(text = 'This search was done by Search Bot')
  await ctx.send(embed = embed)



password = os.environ['password']
bot.run(password)
