import json
import sqlite3 
import hashlib

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

def generate_hash(name, from_set):
	md5 = hashlib.md5()
	md5.update((name + from_set).encode())	
	return md5.hexdigest()

with open('default_cards.json', 'r') as cards:
	cards_obj = json.loads(cards.read())

for card in cards_obj:
	name = card['name']
	quantity = 0 
	from_set = card['set']
	cost = 0
	hash_id = generate_hash(name, from_set)

	cursor.execute('INSERT INTO card_inventory VALUES (?, ?, ?, ?, ?)', [name, quantity, from_set, cost, hash_id])

conn.commit()
