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
maps = [] #for maps
plans = [] #plans

description = '''description'''

class Person:
    def __init__(self, name, m, score, attempts, description, link):
        self.name = name
        self.m = m
        self.score = score
        self.attempts = attempts
        self.description = description
        self.link = link
        #tostring method  def __str__(self):
    def __str__(self):
        return self.m + ',' + self.name + ',' + str(self.score) + ',' + str(self.attempts) + ',' + self.description + ',' + self.link
    def plist(self):
        return [self.m,self.name,str(self.score),str(self.attempts),self.description,self.link]

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
            m = csvreader[r][0]
            score = int(csvreader[r][2])
            attempts = int(csvreader[r][3])
            description = csvreader[r][4]
            link = csvreader[r][5]
            plans.append(Person(name = name, m=m, score = score, attempts=attempts, description=description, link=link))
            plans.sort(key=lambda x: x.m, reverse=False)
            if maps.count(m)==0: maps.append(m)
            r = r+1
        

@bot.command()
async def plus1(ctx, name):
    '''updates the strat with a success'''
    error = 1
    i=0
    for x in plans:
        if plans[i].name == name: 
            plans[i].score+=1
            plans[i].attempts+=1
            await ctx.send(f'PLUS ONE FOR THE STRAT! {name} was successful! Attempts and success rate have been updated. {name} has been attempted {plans[i].attempts} and was successful {plans[i].score} times')
            error = 0
        i+=1
    if error == 1: 
            await ctx.send(f'{name} is not a strat. Please use the plans full name in quotes if there are spaces')
            return
    with open("Strat.csv","w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        update = list(plans)
        stringplans = [x.plist() for x in plans]
        print(stringplans)
        csvwriter.writerows(stringplans)
        
@bot.command()
async def failure(ctx, name):
    '''updates the strat with a success'''
    error = 1
    i=0
    for x in plans:
        if plans[i].name == name: 
            plans[i].attempts+=1
            await ctx.send(f'FAILURE :( {name} wasn\'t successful! Attempts and success rate have been updated. {name} has been attempted {plans[i].attempts} and has failed {plans[i].attempts - plans[i].score} times')
            error = 0
        i+=1
    if error == 1: 
            await ctx.send(f'{name} is not a strat. Please use the plans full name in quotes if there are spaces')
            return
    with open("Strat.csv","w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        update = list(plans)
        stringplans = [x.plist() for x in plans]
        print(stringplans)
        csvwriter.writerows(stringplans)
        

@bot.command()
async def update(ctx, cur_page, message):
    '''updates the message'''
    pages = len(plans)
    if plans[cur_page-1].attempts == 0: percentage = 0
    else: percentage = plans[cur_page-1].score/plans[cur_page-1].attempts*100
    await message.edit(content=f"Page {cur_page}/{pages}: {plans[cur_page-1].m}\n\nName :{plans[cur_page-1].name}\n\nStrat Wins: {plans[cur_page-1].score} Winrate: {percentage}%\n\nDescription: {plans[cur_page-1].description}\n\nLink: {plans[cur_page-1].link}")


@bot.command()
async def strats(ctx):
    contents = maps
    pages = len(plans)
    cur_page = 1
    if plans[cur_page-1].attempts == 0: percentage = 0
    else: percentage = plans[cur_page-1].score/plans[cur_page-1].attempts*100
    message = await ctx.send(f"Page {cur_page}/{pages}: {plans[cur_page-1].m}\n\nName :{plans[cur_page-1].name}\n\nStrat Wins: {plans[cur_page-1].score} Winrate: {percentage}%\n\nDescription: {plans[cur_page-1].description}\n\nLink: {plans[cur_page-1].link}")
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check(reaction, user):
        return str(reaction.emoji) in ["◀️", "▶️", "✅", "❌"]
        

    while True:
            reaction, user = await bot.wait_for("reaction_add", timeout=6000, check=check)
            # waiting for a reaction to be added - times out after x seconds, 6000 in this

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await update(ctx, cur_page, message)
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await update(ctx, cur_page, message)
                await message.remove_reaction(reaction, user)
                
            elif str(reaction.emoji) == "✅":
                await plus1(ctx, plans[cur_page-1].name)
                await update(ctx, cur_page, message)
                await message.remove_reaction(reaction, user)
                
            elif str(reaction.emoji) == "❌":
                await failure(ctx, plans[cur_page-1].name)
                await update(ctx, cur_page, message)
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
                await ctx.send(f'ERROR!')
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        
    
bot.run(TOKEN)