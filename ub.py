# ub.py - untitledbot
# Rebuilt from the ground up

# Import stuff
import datetime
import discord
import asyncio
import sqlite3
import os, sys

# Create connection to database
db	= sqlite3.connect('ub_main.db')
cur	= db.cursor()

# Set constant strings
ub_prefix = 'u.'
ub_text_help = '''**untitledbot by Amity**
untitledbot is a utility bot, with community management, moderation, and other functions.

All commands must start with `u.`. EG: `u.help`.

**Basics**
`help`: Shows this fantastic list of commands.

**Utility**
`notifyme [x]`: Ping you if a message is sent in the current channel, optionally within `x` minutes. `x` defaults to 5. 
`youtube x`: Search for `x` on YouTube. Sends back the top 3 links.
`soundcloud x`: Search for `x` on SoundCloud. Sends back the top 3 links.

**Gaming**
`iown`: Presents a list of games. Set which games you own, so other members can request to play.
`play`: Presents your list of owned games. Select one, and find online (and non-busy) members who own it.
`bored`: Suggests a random game from your library.

**Moderation**
`mute @abc#1234 [x]`: Mute the member "@abc#1234" in the current server for `x` minutes. `x` defaults to 10.
`kick @abc#1234 [x]`: Kick the member "@abc#1234" from the current server, with an optional reason (`x`).
`ban @abc#1234 x y`: Ban the member "@abc#1234" from the current server for `x` hours, with the reason `y`.
'''

# Initialize the Discord API
client = discord.Client()

@client.event
def on_message(message):
	# COMMANDS

	# -- Basics
	if message.startswith(ub_prefix + 'help'):
		await client.delete_message(message)
		await res = client.send_message(message.author, ub_text_help)

	# -- Utility
	elif message.startswith(ub_prefix + 'notifyme'):
		curtime = datetime.now() # todo: fix
		await client.delete_message(message)
		if 'there\'s another message':
			await res = client.send_message(message.channel, 'Someone spoke, {:s}!'.format(message.author.mention))

	# -- Moderation
	elif message.startswith(ub_prefix + 'mute'):
		args = message.content.split(' ')
		if 'is valid member':
			global_muted_members.add() # find member by discord tag, mute
		await client.delete_message(message)

	elif message.startswith(ub_prefix + 'kick'):
		args = message.content.split(' ')
		if 'is valid member':
			client.kick() # find member by discord tag, kick

	# MANAGING MESSAGES

	# -- Moderation
	await for muted_member in global_muted_members:
		# Check timing
		if (message.author == muted_member['member']):
			if (muted_member['time_unmute'] >= datetime.now()): #todo: check, fix
				await global_muted_members.remove(muted_member) #todo: check, fix
			else
				await client.delete_message(message)


# Run the bot
client.run(os.environ['DISCORD_TOKEN_UB'])