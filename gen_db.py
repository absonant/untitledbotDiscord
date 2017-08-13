# Generate the database for untitledbot

import os
import sqlite3

db_name = 'ub_main.sqlite'

if (os.exists(db_name)):
	print ('ub_main.sqlite already exists. If it\'s empty, delete it and run this again.')
	exit()

db_conn = sqlite3.connect(db_name)
c		= db_conn.cursor()

c.execute('''CREATE TABLE server
	# Discord's ID of the server
	(id			TEXT PRIMARY KEY	NOT NULL,
	# Our name of the server
	name		TEXT				DEFAULT=\'Server\',
	# Date we joined the server (2000-12-31)
	joindate	TEXT				NOT NULL,
	# Date and time we last used the server (2000-12-31 01:02)
	lastactive	TEXT				NOT NULL,
	# Permissions - The server owner's Discord ID
	perm_owner_id	TEXT			NOT NULL,
	# Permissions - If the server owner doesn't want to manage the bot, a role can be assigned to do that instead
	perm_role_devel	TEXT,
	# Permissions - Administrator role
	perm_role_admin	TEXT,
	# Permissions - Moderator role
	perm_role_mod	TEXT,
	# Custom information fields, set by server
	field_rules		TEXT,
	field_channels	TEXT,
	field_more		TEXT,
	# Member tagging prefix (a-z only)
	field_tag_pre	TEXT
	);''')

c.execute('''CREATE TABLE member
	# ID of the server that the member belongs to
	(server_id	TEXT				NOT NULL,
	# Member's Discord ID
	id			TEXT PRIMARY KEY	NOT NULL,
	# Member's tags with server-specified prefixes, separated by commas
	tags_csv	TEXT,
	muted		INT,
	unmute_time	TEXT
	);''')

#c.execute('''CREATE TABLE alerts ();''')
