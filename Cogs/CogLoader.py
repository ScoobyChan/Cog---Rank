# Credits to:
# CorpNewt
# CorpBot

# This Module is for loading and managing the Cogs
import os
import discord
from discord.ext import commands 

class CogLoader(commands.Cog):
	print('CogLoader Up')

	def __init__(self, bot):
		self.bot = bot


	def _load_extension(self):
		print('Loading Cogs')
		# Used for testing
		# self.bot.load_extension('Cogs.ping')
		# Directory = 'Cogs/'
		Directory = 'Cogs/'
		cogList = []
		cogListDirectory = os.listdir(Directory)
		print('Cog Files loaded')
		# Used to make sure Directory and file is there

		for name in cogListDirectory:
			if name != '__pycache__' and name != 'CogLoader.py':
				# Splits the 
				ext_name = name.split('.')
				# Sets to integer and gets length of List
				num = ext_name[int(len(ext_name))-1]
				if num == 'py':
					# Checks the Name of the Extension
					print(' - '+ext_name[0])
					# Adds Name to List
					cogList.append(ext_name[0])

		for lname in cogList:
			try:
				# Loads the Cogs
				self.bot.load_extension('Cogs.'+lname)
				# bot.load_extension(cogList)
			except Exception as error:
				print('{} cannot be loaded. [{}]'.format(lname, error))
		print('')

	def _unload_extension(self):
		print('Unloading cogs')
		# Unloads
		Directory = 'Cogs/'
		cogList = []
		cogListDirectory = os.listdir(Directory)
		print('Cog Files unloaded')
		# Used to make sure Directory and file is there

		for name in cogListDirectory:
			if name != '__pycache__' and name != 'CogLoader.py':
				# Splits the 
				ext_name = name.split('.')
				# Sets to integer and gets length of List
				num = ext_name[int(len(ext_name))-1]
				if num == 'py':
					# Checks the Name of the Extension
					print(' - '+ext_name[0])
					# Adds Name to List
					cogList.append(ext_name[0])

		for uname in cogList:
			try:
				# Loads the Cogs
				self.bot.unload_extension('Cogs.'+uname)
				# bot.load_extension(cogList)
			except Exception as error:
				print('{} cannot be unloaded. [{}]'.format(uname, error))
		print('')

	@commands.command()
	async def reload(self, ctx):
		print('Reloading cogs')
		# Admins only
		# Unloads
		self._unload_extension()
		self._load_extension()

		await ctx.send('Cogs Successfully reloaded') # send to logs

	# Tester Only
	# @commands.command()
	# async def test(self, ctx):
	# 	print('testing theory')
	# 	self._unload_extension()

	# Tester Only
	@commands.command()
	async def load(self, ctx):
		self._load_extension()
		await ctx.send('Cogs Successfully loaded') # Send to logs

	# Tester Only
	@commands.command()
	async def unload(self, ctx):
		self._unload_extension()
		await ctx.send('Cogs Successfully unloaded') # Send to logs

def setup(bot):
	bot.add_cog(CogLoader(bot))
