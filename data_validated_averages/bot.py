import discord

class DiscordClient(discord.Client):
	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))

	async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('NzIwNjM2NDI2MDQ3MTkzMTI4.XuI4Eg.04ZDjvNcUoAS3ChIT51yCP_0IMs')