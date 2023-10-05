# bot.py
from asyncio.windows_events import NULL
import os
import random
from re import L
from token import EQUAL
from discord.ext import commands
from discord.ui import view 
import discord
import csv

TOKEN = 'REDACTED'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
rows = [] #for initialization
maps = [] #for updating
people = [] #strats
KD = [] #Kafe
CO = [] #Coastline
OR = [] #Oregon
CH = [] #Chalet

description = '''description'''

class Person:
    def __init__(self, name, map, score, attempts, description, link):
        self.name = name
        self.map = map
        self.score = 0
        self.attempts = attempts
        self.description = description
        self.link = link

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    with open("Strat.csv","r+", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvreader = csv.reader(csvfile, delimiter=',')
        csvreader = list(csvreader)
        r = 0;
        n = 0; #keep track of any new entries added
        for row in csvreader:
            if csvreader[r][0] == []: break
            name = csvreader[r][1]
            map = csvreader[r][0]
            score = int(csvreader[r][2])
            attempts = int(csvreader[r][3])
            description = csvreader[r][4]
            link = csvreader[r][5]
            people.append(Person(name = name, map=map, score = score, attempts=attempts, description=description, link=link))
            #print(f'{people[name].name} has {people[name].score} points')
            #update.append([people[name].name,people[name].score])
            people.sort(key=lambda x: x.map, reverse=False)
            if maps.count(map)==0: maps.append(map)
            if map=="Kafe Dostoyevsky": KD.append(name)
            if map=="Coastline": CO.append(name)
            if map=="Oregon": OR.append(name)
            if map=="Chalet": CH.append(name)
            r = r+1

       
@bot.command()
async def members(ctx):
    '''Server Members.'''
    x = ctx.guild.members
    for member in x:
        await ctx.send(f'{member.name} is also called {member.nick}')

@bot.command()
async def strats(ctx):
    #contents = ["Kafe Dostoyevsky", "Coastline", "Oregon", "Chalet"]
    contents = maps
    pages = len(people)
    cur_page = 1
    if people[cur_page-1].attempts == 0: percentage = 0
    else: percentage = people[cur_page-1].score/people[cur_page-1].attempts*100
    message = await ctx.send(f"Page {cur_page}/{pages}: {people[cur_page-1].map}\n\nName :{people[cur_page-1].name}\n\nStrat Wins: {people[cur_page-1].score} Winrate: {percentage}%\n\nDescription: {people[cur_page-1].description}\n\nLink: {people[cur_page-1].link}")
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return str(reaction.emoji) in ["◀️", "▶️"]
        

    while True:
            reaction, user = await bot.wait_for("reaction_add", timeout=6000, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                if people[cur_page-1].attempts == 0: percentage = 0
                else: percentage = people[cur_page-1].score/people[cur_page-1].attempts*100
                await message.edit(content=f"Page {cur_page}/{pages}: {people[cur_page-1].map}\n\nName :{people[cur_page-1].name}\n\nStrat Wins: {people[cur_page-1].score} Winrate: {percentage}%\n\nDescription: {people[cur_page-1].description}\n\nLink: {people[cur_page-1].link}")
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                if people[cur_page-1].attempts == 0: percentage = 0
                else: percentage = people[cur_page-1].score/people[cur_page-1].attempts*100
                await message.edit(content=f"Page {cur_page}/{pages}: {people[cur_page-1].map}\n\nName :{people[cur_page-1].name}\n\nStrat Wins: {people[cur_page-1].score} Winrate: {percentage}%\n\nDescription: {people[cur_page-1].description}\n\nLink: {people[cur_page-1].link}")
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        
    
bot.run(TOKEN)


