import discord
from discord.ext import commands

class default(commands.Cog):
	# print('Fun Cog Working')
	def __init__(self, bot):
		self.bot = bot

	# async def on_message(self, message):
	# 	await self.bot.send('message')

	@commands.command()
	async def default(self, ctx):
		print('default')

def setup(bot):
	bot.add_cog(invite(bot))