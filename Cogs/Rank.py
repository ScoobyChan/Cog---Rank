import discord
import random
import asyncio
from discord.ext import commands

import sqlite3
conn = sqlite3.connect('importantFiles/botDatabase.db')
c = conn.cursor()

class Rank(commands.Cog):
	# loop to use up feed if enabled
	c.execute('CREATE TABLE IF NOT EXISTS Rank (ID INTEGER PRIMARY KEY AUTOINCREMENT, ServerID INTEGER, rankName text, RankPoints INTEGER)')
	c.execute('CREATE TABLE IF NOT EXISTS Members (ID INTEGER PRIMARY KEY AUTOINCREMENT, ServerID INTEGER, UserID INTEGER, xpreserve INTEGER, xp INTEGER, role TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS Bot (serverID text UNIQUE, serverOwner text, adminRole text, moderatorRole text, logChannel text, commandChannal text, welcomeChannel text, honkChannel text, defaultRole text, reportingChannel text, DJRole text, feed int)')
	c.execute('CREATE TABLE IF NOT EXISTS XP(ID INTEGER PRIMARY KEY AUTOINCREMENT, serverID INTEGER, xpCap INTEGER, enableXP text, xpgain INTEGER)')

	conn.commit()
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		numOne = random.randint(0, 50)
		numTwo = random.randint(0, 50)

		guild= message.guild.id
		author = message.author.id
		serverInc = 1 # make change able

		if numTwo == numOne:
			print('true')
			try:
				c.execute("SELECT * FROM User WHERE ServerID={} AND UserID={}".format(guild, author))
				user = c.fetchall()
			except:
				print('User err')
				return

			curXP = user[0][3] # check xp posisition
			xp = curXP + serverInc
			
			try:
				c.execute('UPDATE User SET xp={}, role="{}" WHERE ServerID={} AND UserID={}'.format(xp, chRank, guild, author))
				conn.commit()
			except:
				print('User err')
				return
	
	@commands.command()
	async def enableXP(self, ctx): # Check if enabled or disabled
		try:
			c.execute("SELECT * FROM XP WHERE serverID={}".format(ctx.guild.id))
			en = c.fetchall()
			enabled = en[0][3]
		except:
			print('User err')
			return

		if enabled == 'Enable':
			enable = 'Disable'
		else:
			enable = 'Enable'

		c.execute("UPDATE XP SET enableXP='{}' WHERE serverID={}".format(enable, ctx.guild.id))
		conn.commit()
		await ctx.send(f"XP enable set to: **{enable}d**")

	@commands.command()
	async def xpgain(self, ctx, xpgain:int):
		try:
			c.execute("UPDATE XP SET xpgain={} WHERE serverID={}".format(xpgain, ctx.guild.id))
			conn.commit()
			await ctx.send(f"XP gain set to: {str(xpgain)}")
		except:
			print('XP gain Error')

	@commands.command()
	async def xpCap(self, ctx, xpCap:int):
		serverID = ctx.guild.id
		if xpCap < 50:
			await ctx.send('Cap too low please be higher than or equal too **50**')
			return
		
		try:
			c.execute("UPDATE XP SET xpCap={} WHERE serverID={}".format(xpCap, serverID))
			conn.commit()
			await ctx.send(f"XP cap set to: {str(xpCap)}")
		except:
			print('xpCap error')

	@commands.command()
	async def xpregen(self, ctx, mem:str):
		member = int(mem.strip('<>@'))
		serverID = ctx.guild.id

		try:
			c.execute("UPDATE Members SET xpreserve=100000 WHERE ServerID={} AND UserID={}".format(serverID, member))
			conn.commit()
			await ctx.send(f"<@{member}> has been given 100,000 XP")
		except:
			return await ctx.send(f'No user with ID: {str(member)}')

	@commands.command()
	async def xp(self, ctx, mem:str, xp:int):
		serverID = ctx.guild.id
		member = int(mem.strip('<@>'))
		# need to check for User
		try:
			c.execute("SELECT * FROM Members WHERE ServerID={} AND UserID={}".format(serverID, member))
		except:
			await ctx.send(f"No user ID: {str(member)}")
			return
		
		authorID = ctx.author.id
		# check if admin
		if authorID == member:
			await ctx.send('You do not have permissions to give XP to yourself')
			return

		if xp < 0: # get to check if owner amd admin later
			await ctx.send("You can't take away XP")

		# Member
		try:
			c.execute("SELECT * FROM Members WHERE UserID={} AND ServerID={}".format(member, serverID))	
			demo = c.fetchall()
			TonewXP = demo[0][4] + xp
		except:
			print('To Member Error')
			return

		# User
		try:
			c.execute("SELECT * FROM Members WHERE UserID={} AND ServerID={}".format(authorID, serverID))	
			demo = c.fetchall()
			FromNewXP = demo[0][3] - xp
		except:
			print('From Member Error')
			return

		if FromNewXP < 0:
			return await ctx.send(f"<@{authorID}> you have insufficioent XP")
		
		try:
			c.execute("UPDATE Members SET xp={} WHERE ServerID={} AND UserID={}".format(int(TonewXP), serverID, member))
			c.execute("UPDATE Members SET xpreserve={} WHERE ServerID={} AND UserID={}".format(FromNewXP, serverID, authorID))
			conn.commit()
			await ctx.send(f'<@{authorID}> has given XP')
		except:
			print('err')
			await ctx.send('Error giving XP')
			return


# ####################  semi tested  ###########################
	@commands.command()
	async def addMember(self, ctx, mem:str):
		try:
			c.execute("SELECT * FROM Bot WHERE serverID={}".format(ctx.guild.id))
			en = c.fetchall()
			bot = en[0][8]
		except:
			print('Bot err')
			return

		member = int(mem.strip('<>@'))

		try:
			c.execute("SELECT * FROM Members WHERE serverID={} AND UserID={}".format(ctx.guild.id, member))
			en = c.fetchall()
		except:
			print('Is a user')
		
		if not en == []:
			await ctx.send('User alread in database')
			return

		try:
			c.execute('INSERT INTO Members(ServerID, UserID, xpreserve, xp, role) VALUES ({},{},0,0,"{}")'.format(ctx.guild.id, member, bot)) # f"{member.id}"
			conn.commit()
			await ctx.send('I have added the user to my database')
		except:
			await ctx.send('User Alreadyin server')
			return

	@commands.command()
	async def feed(self, ctx, ammount: int): # Change to use feed database not xp
		try:
			c.execute('SELECT * FROM Members WHERE ServerID={} AND UserID={}'.format(ctx.guild.id, ctx.author.id))
			befUser = c.fetchall()
		except:
			print('Error')
			return

		guild = ctx.guild.id
		author = ctx.author.id
		bot = self.bot.user.id

		if befUser[0][3] < ammount:
			await ctx.send(f"Insufficient funds, please don't try my intelligents <@{ctx.author.id}>\nYou only have: **{str(demo[0][3])}**")
			return

		afterUser = befUser[0][3] - ammount

		# Bot
		try:
			c.execute('SELECT * FROM Bot WHERE serverID="{}"'.format(str(ctx.guild.id)))
			beforeBot = c.fetchall()
			afterBot = beforeBot[0][11] + ammount
		except:
			print("Bot error")


		# User
		try:
			c.execute('UPDATE Members SET xp={} WHERE ServerID={} AND UserID={}'.format(afterUser, guild, author))
			conn.commit()
		except:
			print('User err')
			return

		# Bot
		try:
			c.execute('UPDATE Bot SET feed={} WHERE serverID={}'.format(afterBot, str(ctx.guild.id)))
			conn.commit()
		except:
			print('Bot err')
			return




		if afterBot < 40:
			await ctx.send(f'hmmm that was tastey, I am still hungry though <@{ctx.author.id}>')
			return

		if afterBot > 200:
			await ctx.send(f'hmmm that was tastey, I am now satisfied because of <@{ctx.author.id}>')
			return

		if afterBot > 400:
			await ctx.send(f'hmmm that was tastey, <@{ctx.author.id}> has over feed me')
			return

		await ctx.send(f'hmmm that was tastey, thanks <@{ctx.author.id}> for feeding me **{str(ammount)}**')

# 	@commands.command()
# 	async def promote(self, ctx, __user: str, _rank: str):
# 		_user = str(__user).strip('<>@')
# 		user = int(_user)
# 		server = ctx.guild.id

# 		try:
# 			c.execute("SELECT * FROM User WHERE ServerID={} AND UserID={}".format(server, user))
# 			_user = c.fetchall()
# 		except:
# 			print('User err')
# 			return

# 		if str(_user) == '[]':
# 			await ctx.send('User not in database')
# 			return

# 		roleUser = _user[0][5]
		
# 		if roleUser == _rank:
# 			await ctx.send("User Already this role")
# 			return

		
# 		if str(_rank) != 'False':
# 			try:
# 				c.execute("SELECT * FROM Rank WHERE ServerID={} AND rankName='{}'".format(server, _rank))
# 				_Rank = c.fetchall()
# 			except:
# 				print('Rank err')
# 				return

# 			if str(_Rank) == '[]':
# 				await ctx.send('Role not in database')
# 				return

# 			user = user[0][2]
# 			xp = _Rank[0][3]

# 		else:
# 			_rank = _user[0][5]
# 			try:
# 				c.execute("SELECT * FROM Rank WHERE ServerID={} AND rankName='{}'".format(server, _rank))
# 				_Rank = c.fetchall()
# 			except:
# 				print('Rank err')
# 				return
# 			_Rank = _Rank[0][3]

# 			try:
# 				c.execute("SELECT * FROM Rank WHERE ServerID={}".format(server))
# 				_Ranks = c.fetchall()
# 			except:
# 				print('Rank err')
# 				return

# 			chRank = ''

# 			for Ranks in _Ranks:
# 				if Ranks[3] > _Rank:
# 					chRank = Ranks[2]
# 					xp = Ranks[3]
# 					break
				
# 				if Ranks[3] >= 10000:
# 					xp = Ranks[3]
# 					break

# 			print(xp)
# 			print(chRank)

# 		if chRank != '':
# 			c.execute('UPDATE User SET xp={}, role="{}" WHERE ServerID={} AND UserID={}'.format(xp, chRank, server, user))
# 			conn.commit()

# 		try:
# 			c.execute("SELECT * FROM User WHERE ServerID={} AND UserID={}".format(server, user))
# 			user = c.fetchall()
# 		except:
# 			print('User err')
# 			return

# 		try:
# 			role = discord.utils.get(member, name=userRole)
# 			await bot.add_roles(user, role)
# 		except:
# 			return	

# 		if chRank == '':
# 			msg = f'<@{user[0][2]}> at the top rank like a Cool Guy 😎'
# 		else:
# 			msg = f'<@{user[0][2]}> has been Promoted to **{_rank}**'

		

# 		embed=discord.Embed(color=0xd54ac7)
# 		embed.add_field(name="Promotion Time", value=msg, inline=False)
# 		await ctx.send(embed=embed)

# 	@commands.command()
# 	async def demote(self, ctx, __user: str, _rank: str):
# 		_user_ = str(__user).strip('<>@')
# 		user = int(_user_)
# 		server = ctx.guild.id
# 		chRank = ''
		
# 		try:
# 			c.execute("SELECT * FROM User WHERE ServerID={} AND UserID={}".format(server, user))
# 			_user = c.fetchall()
# 		except:
# 			print('User err')
# 			return

# 		if str(_user) == '[]':
# 			await ctx.send('User not in database')
# 			return

# 		roleUser = _user[0][5]
		
# 		if roleUser == _rank:
# 			await ctx.send("User Already this role")
# 			return

# 		try:
# 			c.execute('SELECT * FROM Rank WHERE ServerID={}'.format(ctx.guild.id))
# 			demo = c.fetchall()
# 			rank = demo[0][2]
# 		except:
# 			print('cant access db')
		
# 		print(_user[0][5])
# 		print(rank)

# 		if _user[0][5] == rank:
# 			msg = f'<@{_user[0][2]}> at the Bottom rank 😎'

# 			embed=discord.Embed(color=0xd54ac7)
# 			embed.add_field(name="Demotion Time", value=msg, inline=False)
# 			await ctx.send(embed=embed)
# 			return


# 		if str(_rank) != 'False':
# 			try:
# 				c.execute("SELECT * FROM Rank WHERE ServerID={} AND rankName='{}'".format(server, _rank))
# 				_Rank = c.fetchall()
# 			except:
# 				print('Rank err')
# 				return

# 			if str(_Rank) == '[]':
# 				await ctx.send('Role not in database')
# 				return

# 			xp = _Rank[0][3]

# 		else:
# 			_rank = _user[0][5]
			
# 			try:
# 				c.execute("SELECT * FROM Rank WHERE ServerID={}".format(server))
# 				_Rank = c.fetchall()
# 			except:
# 				print('Rank err')
# 				return
			
# 			chRank = ''
# 			for _rank_ in _Rank:
# 				if str(_rank_[2]) == str(_rank):
# 					break

# 				chRank = _rank_
		
# 			xp = chRank[3]
# 			chRank = chRank[2]
		
		
# 		c.execute('UPDATE User SET xp={}, role="{}" WHERE ServerID={} AND UserID={}'.format(xp, chRank, server, user))
# 		conn.commit()

# 		try:
# 			c.execute("SELECT * FROM User WHERE ServerID={} AND UserID={}".format(server, user))
# 			fUser = c.fetchall()
# 		except:
# 			print('User err')
# 			return

# 		# try:
# 		# 	role = discord.utils.get(member, name=userRole)
# 		# 	await bot.add_roles(user, role)
# 		# except:
# 		# 	return	

		
# 		msg = f'<@{fUser[0][2]}> has been Demoted to **{chRank}**'

# 		embed=discord.Embed(color=0xd54ac7)
# 		embed.add_field(name="Demotion Time", value=msg, inline=False)
# 		await ctx.send(embed=embed)

# 	@commands.command()
# 	async def ranks(self, ctx):
# 		user = ctx.author.name
# 		c.execute('SELECT * FROM Rank WHERE ServerID={}'.format(ctx.guild.id))
# 		demo = c.fetchall()
# 		msg = ''

# 		for servRank in demo:
# 			RankName = servRank[2]
# 			RankPoint = servRank[3]
# 			msg += ' - **' + RankName + '** with XP count required of: **' + str(RankPoint) + '**\n'

# 		embed=discord.Embed(color=0xd54ac7)
# 		embed.add_field(name="Servers Ranks", value=msg, inline=False)
# 		embed.set_footer(text=f"requested by: {user}")
# 		await ctx.send(embed=embed)

	@commands.command()
	async def aRank(self, ctx, rank: int, *, name: str): # add colors
		
		c.execute('SELECT * FROM Rank WHERE ServerID={}'.format(ctx.guild.id))
		demo = c.fetchall()
		if demo != '[]':
			for servRank in demo:
				if rank <= servRank[3]:
					await ctx.send('Rank XP needs to be higher than before rank')
					return

				if servRank[2].lower() == name.lower():
					await ctx.send('Rank Name needs to be different')
					return

			c.execute('INSERT INTO Rank (ServerID, rankName, RankPoints) VALUES ({}, "{}", {})'.format(ctx.guild.id, name, rank))
			conn.commit()

			await ctx.guild.create_role(name=name, colour=discord.Colour(0xda3c3c)) # make random color
			await ctx.send(f'Added Rank **{name}**')

	@commands.command()
	async def rRank(self, ctx, name: str):
		serName = ''
		num = 0
		for role in ctx.guild.roles:
			if str(role) == name:
				serName = role
				detail = num

			num += 1

		if serName != '':
			await ctx.guild.roles[detail].delete()
			c.execute('DELETE FROM Rank WHERE ServerID={} AND rankName="{}"'.format(ctx.guild.id, name)) # fix
			conn.commit()
			await ctx.send(f'Removed the Role: {name}')
		else:
			await ctx.send(f'No roles under the name: **{name}**')


def setup(bot):
	bot.add_cog(Rank(bot))