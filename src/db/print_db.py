import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

tables = []

for table in cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"'):
	tables.append(table[0])

for table in tables:
	print(table)
	for row in cursor.execute('SELECT * FROM {}'.format(table)):
		print('* ' + str(row))
