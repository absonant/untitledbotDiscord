#!/usr/bin/python

# ub.py - untitledbot
# Rebuilt from the ground up

# Import stuff
import time
import discord
import asyncio
import sqlite3
import os, sys

db_name = 'ub_main.sqlite'

# Create connection to database
if not (os.path.exists(db_name)):
	print('Database doesn\'t exist. Run gen_db.py first to get everything set up.')
	exit()
db_conn	= sqlite3.connect(db_name)
db_cur	= db_conn.cursor()
print('  Opened a database connection on [' + db_name + '].')

# Set constant strings
ub_prefix = 'u.'
ub_text_help = '''**untitledbot by Amity**
untitledbot is a utility bot, with community management, moderation, and other functions.

All commands must start with `u.`. EG: `u.help`.

**Basics**
`help`: Shows this fantastic list of commands.

**Utility**
`notifyme [x]`: Ping you if a message is sent in the current channel, optionally within `x` minutes. `x` defaults to 5. 
`youtube x`: Search for `x` on YouTube. Sends the top 3 links.
`soundcloud x`: Search for `x` on SoundCloud. Sends the top 3 links.
`imgur x`: Search for `x` on imgur. Sends the first result.

**Gaming**
`iown`: Presents a list of games. Set which games you own, so other members can request to play.
`play`: Presents your list of owned games. Select one, and find online (and non-busy) members who own it.
`bored`: Suggests a random game from your library.

**Moderation**
`mute @abc#1234 [x]`: Mute the member "@abc#1234" in the current server for `x` minutes. `x` defaults to 10.
`kick @abc#1234 [x]`: Kick the member "@abc#1234" from the current server, with an optional reason (`x`).
`ban @abc#1234 x y`: Ban the member "@abc#1234" from the current server for `x` hours, with the reason `y`.
'''
ub_text_help_setup = '''**untitledbot - Set Me Up for Your Server**
untitledbot is a utility bot, with community management, moderation, and other functions. I\'ve tried to make it as easy as possible to set up for your server, however it is complicated, so I recommend reading through this: https://github.com/absonant/untitledbotDiscord/README.md
'''

# Initialize the Discord API
client = discord.Client()

class ub_td():
	# ub DateTime
	def get_current_date_str():
		return (time.strftime('%Y-%m-%d', time.gmtime()))
	def get_current_time_str():
		return (time.strftime('%H:%M:%S', time.gmtime()))
	def add(x_date, x_time, y_date, y_time):
		# todo: fix
		return 0

@client.event
def on_message(message):
	# COMMANDS

	# -- Setup

	# -- Basics
	if message.startswith(ub_prefix + 'help'):
		await client.delete_message(message)
		await res = client.send_message(message.author, ub_text_help)
	elif message.startswith(ub_prefix + 'helpsetup'):
		await client.delete_message(message)
		await res = client.send_message(message.author, ub_text_help_setup)

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

@client.event
def on_server_join(server):
	await db_cur.execute('''INSERT INTO server
		(id,
		name,
		joindate,
		lastactive,
		perm_owner_id)
		VALUES (?,?,?,?,?);''', \
		(server.id,
		server.name,
		ub_td.get_current_date_str(),
		(ub_td.get_current_date_str() + ' ' + ub_td.get_current_time_str()),
		server.owner.id))
	# commit changes
	await db_conn.commit()
	await res = client.send_message(server.owner, 'untitledbot now recognises you as the owner of the server "{:s}". \
		If you\'d rather leave bot setup to someone else, please use `u.setup.setdevrole <role_name>`. See the README at \
		https://github.com/absonant/untitledbotDiscord if you need some help setting up.'.format(server.name))

@client.event
def on_ready():
	found = False
	for server in client.servers:
		await c = db_conn.execute('''SELECT id, name from server''')
		for server_in_db in c:
			if (server_in_db[0] == server.id):
				found = True
		# todo: fix before running
		if not found:
			on_server_join(server)


# Run the bot
client.run(os.environ['DISCORD_UB_APITOKEN'])
print(client.name + ' ({:s}) is listening...'.format(client.id))
