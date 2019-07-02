# Credits from CorpBot and CorpNewt
import json 
import asyncio
import time
import discord
import os
from discord.ext import commands
from mcstatus import MinecraftServer

import sqlite3
conn = sqlite3.connect('importantFiles/botDatabase.db')
c = conn.cursor()

# Loads the TOKEN
imp = 'importantFiles/'
if os.path.exists(imp + 'TOKEN.txt'):
	# print('TOKEN Loaded')
	with open(imp + 'TOKEN.txt') as t:
		TOKEN = t.read()
	if not TOKEN:
		# this is temporary
		TOKEN = "nul"

# Loads the PREFIX
if os.path.exists(imp + 'PREFIX.txt'):
	# print('PREFIX Loaded')
	with open(imp + 'PREFIX.txt') as p:
		# reads the file
		PREFIX = p.read()
	if not PREFIX:
		PREFIX = '$'

# Loads the API Keys
if os.path.exists(imp + 'GOOGLEAPI.txt'):
	# print('PREFIX Loaded')
	with open(imp + 'GOOGLEAPI.txt') as p:
		# reads the file
		google_api = p.read()
	if not google_api:
		google_api = 'null'



Bot = discord.Client()

# use this for initialising the Bot but only use for under 5 servers.
# bot = commands.Bot(command_prefix=PREFIX, pm_help=None, description='A bot that does stuff.... probably')
bot = commands.Bot(command_prefix=PREFIX, pm_help=None, description='Just Another Bot... I think', game=" with Scooby Chan", case_insensitive=True)

# use AutoShared for more than 5 servers
# bot = commands.AutoShardedBot(command_prefix=get_prefix, pm_help=None, description='A bot that does stuff.... probably', shard_count=4)

# channel = ctx.message.channel
# author  = ctx.message.author
# server  = ctx.message.guild
# message = ctx.message


@bot.event
async def on_ready():
	print("roBot OnLiNe")
	if not bot.get_cog("CogLoader"):
    	# Borrowed from CorpBot
		print('Logged in as:\n{0} (ID: {0.id})\n'.format(bot.user))
		print("Invite Link:\nhttps://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8\n".format(bot.user.id))
    	# Loading Bot
		bot.load_extension("Cogs.CogLoader")
		cg_load = bot.get_cog('CogLoader')
		cg_load._load_extension()

	activity = discord.Game(name="with Scooby Chan", type=0)
	await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_connect():
	print("Im here")
# Calls Database
# Adds member to Role
# Welcomes the USer

# @commands.has_role("Mod")

@bot.event
async def on_member_join(member):
	# print(serverID)
	# member.id
	serverID = member.guild.id
	author = member.name
	
	# Fetchs Database
	c.execute("SELECT * FROM Bot WHERE serverID='{}'".format(serverID))
	demo = c.fetchall()
	if not demo[0][7] == "None":
		userRole = demo[0][7]
		role = discord.utils.get(member, name=userRole)
		await bot.add_roles(author, role)
	# Sends to Channel if there
	welcome = demo[0][6]
	if not welcome == "None":
		channel = bot.get_channel(int(welcome))
		await channel.send(f'Cheers, love!  **{member.name}** is here! Welcome to  the {member.guild.name} Server.\n Type {PREFIX}help for list of Bot commands. Please Read the rules. \nFailure to Abide to them may lead to a tempBan or Permanent Ban Depending serverity. Thank you')
		c.execute('INSERT INTO Members(MemberID, xp, reserveXp, serverID) VALUES ("{}",0,0,"{}")'.format(member.id, member.guild.id)) # f"{member.id}"
		conn.commit()

@bot.event
async def on_member_leave(member):
	# Fetchs Database
	c.execute("SELECT * FROM Bot WHERE serverID='{}'".format(serverID))
	demo = c.fetchall()

	welcome = demo[0][6]
	if not welcome == "None":
		role = discord.utils.get(member, name=userRole)
		await bot.add_roles(author, role)
		# Sends to Channel if there
		channel = bot.get_channel(int(welcome))
		await channel.send(f"GoodBye {member.name}")

# Initialise Mass Destruction
def run():
	bot.run(TOKEN, bot=True, reconnect=True)

loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(run())
finally:
	print('Bot Closing')
	loop.close()
