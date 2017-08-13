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
	def add_seconds(x_date, x_time, sec):
		x = time.strptime(x_date + ' ' + x_time, '%Y-%m-%d %H:%M:%S')
		return x + time.timedelta(seconds=sec)
	def add_minutes(x_date, x_time, min):
		return add_seconds(x_date, x_time, min*60)

@client.event
def on_message(message):
	# COMMANDS

	# -- Setup
	if message.startswith(ub_prefix + 'setup.setrole'):
		if (message.server.owner == message.author):
			args = message.content.split() # Split by whitespace
			roletype	= args[1]
			rolename	= args[2]

			for role in message.server.roles:
				if role.name.lower() == rolename.lower():
					if (roletype == 'admin'):
						await db_cur.execute('''UPDATE server SET perm_role_admin=\'?\' WHERE id=\'?\'''', (role.id, message.server.id))
						await db_conn.commit()
						await res = client.send_message(message.channel, 'The role "'+ found +'" is now set as administrator. Kick and Mute commands will have no effect.')
					elif (roletype == 'mod' or roletype == 'moderator'):
						await db_cur.execute('''UPDATE server SET perm_role_mod=\'?\' WHERE id=\'?\'''', (role.id, message.server.id))
						await db_conn.commit()
						await res = client.send_message(message.channel, 'The role "'+ found +'" is now set as moderator. The Mute command will have no effect.')
					elif (roletype == 'dev' or roletype == 'developer'):
						await db_cur.execute('''UPDATE server SET perm_role_devel=\'?\' WHERE id=\'?\'''', (role.id, message.server.id))
						await db_conn.commit()
						await res = client.send_message(message.channel, 'The role "'+ found +'" is now set as developer. \
							**This is a very dangerous operation.** If you didn\'t mean to do this, execute `u.setup.unsetrole <ub_roletype>` **NOW** to revert.\
							See https://github.com/absonant/untitledbotDiscord/README.md for more info.')
		else:
			print('Non-owner '+ message.author.id +' tried to set roles.')

	elif message.startswith(ub_prefix + 'setup.unsetrole'):
		if (message.server.owner == message.author):
			args = message.content.split()
			rolename	= args[1]
			if (rolename == 'admin'):
				await db_cur.execute('''UPDATE server SET perm_role_admin=\'\' WHERE id=\'?\'''', (message.server.id))
			if (rolename == 'mod' or rolename == 'moderator'):
				await db_cur.execute('''UPDATE server SET perm_role_mod=\'\' WHERE id=\'?\'''', (message.server.id))
			if (rolename == 'dev' or rolename == 'developer'):
				await db_cur.execute('''UPDATE server SET perm_role_devel=\'\' WHERE id=\'?\'''', (message.server.id))
		else:
			print('Non-owner '+ message.author.id +' tried to set roles.')

	# -- Basics
	elif message.startswith(ub_prefix + 'help'):
		await client.delete_message(message)
		await res = client.send_message(message.author, ub_text_help)
	elif message.startswith(ub_prefix + 'helpsetup'):
		await client.delete_message(message)
		await res = client.send_message(message.author, ub_text_help_setup)

	# -- Utility
	#elif message.startswith(ub_prefix + 'notifyme'):
	#	curtime = datetime.now() # todo: fix
	#	await client.delete_message(message)
	#	if 'there\'s another message':
	#		await res = client.send_message(message.channel, 'Someone spoke, {:s}!'.format(message.author.mention))

	# -- Moderation
	#elif message.startswith(ub_prefix + 'mute'):
		#args = message.content.split()
		#name_to_mute = args[1]
		# todo ----
		# Check if the member is in our list of known members. If not, add them. Either way, update their fields so they're muted
		# time_to_mute should be added to the current time, then put into the database in the correct format
		# ---------
		#time_to_mute = args[2]

	#elif message.startswith(ub_prefix + 'kick'):
	#	# check if the author is a moderator
	#	args = message.content.split(' ')
	#	if 'is valid member':
	#		client.kick() # find member by discord tag, kick

	# MANAGING MESSAGES

	# -- Moderation
	# Mute function
	if not (message.server == None): # If the message wasn't sent in a server, don't bother checking. If it was...
		c = db_cur.execute('''SELECT combo_id, id, server_id, muted, unmute_time FROM member WHERE server_id=\'?\'''', message.server.id)
		for member_ref in c: # For every member on the current server
			if member_ref[3] == 1: # If muted
				print('Deleting message from '+message.author.id+' - member is muted')
				client.delete_message(message)


@client.event
def on_server_join(server):
	print('Adding server '+ server.name +' ('+ server.id +') to database...')
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
	print('    Done!')
	#print('Archiving members...')

@client.event
def on_ready():
	await client.change_presence(game=discord.Game(name='on {:i} servers!'.format(len(client.servers))))

	for connected_server in client.servers:
		await c = db_conn.execute('''SELECT id from server where id=\'?\'''', connected_server.id)
		if len(c) == 0:
			print('Adding previously joined server "'+ connected_server.name +'" to database.')
			await on_server_join(server) # I really hope this works lol / todo: test

# Run the bot
client.run(os.environ['DISCORD_UB_APITOKEN'])
print(client.user.name + ' ({:s}) is listening...'.format(client.user.id))
