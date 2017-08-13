# Generate the database for untitledbot

import os
import sqlite3

db_name = 'ub_main.sqlite'

if (os.path.exists(db_name)):
	print ('ub_main.sqlite already exists. If it\'s empty, delete it and run this again.')
	exit()

db_conn = sqlite3.connect(db_name)
c		= db_conn.cursor()

# Discord's ID of the server
# Name of the server
# Date we joined the server (2000-12-31)
# Date and time we last used the server (2000-12-31 01:02)
# Permissions - The server owner's Discord ID
# Permissions - If the server owner doesn't want to manage the bot, a role can be assigned to do that instead
# Permissions - Administrator role
# Permissions - Moderator role
# Custom information fields, set by server
# Member tagging prefix (a-z only)
c.execute('''CREATE TABLE server(
	id				TEXT PRIMARY KEY	NOT NULL,
	name			TEXT				NOT NULL,
	joindate		TEXT				NOT NULL,
	lastactive		TEXT				NOT NULL,
	perm_owner_id	TEXT				NOT NULL,
	perm_role_devel	TEXT,
	perm_role_admin	TEXT,
	perm_role_mod	TEXT,
	field_rules		TEXT,
	field_channels	TEXT,
	field_more		TEXT,
	field_tag_pre	TEXT);''')

# ID of the server that the member belongs to
# Member's Discord ID
# Member's tags with server-specified prefixes, separated by commas
# Is the member muted? (bool)
# Date & time the member should be unmuted (2000-12-31 01:02)
c.execute('''CREATE TABLE member
	(server_id		TEXT				NOT NULL,
	id				TEXT PRIMARY KEY	NOT NULL,
	tags_csv		TEXT,
	muted			INT,
	unmute_time		TEXT);''')

#c.execute('''CREATE TABLE alerts ();''')

db_conn.commit()
print('All done! Closing connection and exiting...')
db_conn.close()
exit()
