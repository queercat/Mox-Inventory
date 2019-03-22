#!/usr/local/bin/python3
# Mox Inventory -- A Scryfall powered opensource MTG invetory utility.

import json # Handles JSON data.
import sqlite3 # Backend DB for MOXI.
import card # A utility for creating and handling magic cards.
import requests # Handles even more web reqs.
import flask # Awesome microservice for handling web reqs.
import hashlib # Creating hashes for card IDs.

app = flask.Flask(__name__)

@app.route('/cards/add', methods = ['GET'])
def handle_add():
	print('')	

with open('config.json', 'r') as config_file:
	config_obj = json.loads(config_file.read())

db_location = config_obj['db_location']

# Loads the DB and returns a cursor.
def init_db():
	conn = sqlite3.connect(db_location)
	return conn, conn.cursor()

# Variables for the conn and cursor the the DB.
conn, cursor = init_db()

# Update DB ... Commits changes to DB.
def update_db(info):
	conn.execute('INSERT INTO db_interactions VALUES (?)', [info])
	conn.commit()

# Hashes using MD5 from name and set to generate a unique ID.
def generate_hash(name, from_set):
	md5 = hashlib.md5()
	md5.update((name + from_set).encode())
	return md5.hexdigest() 

# Adds a card to the inventory DB.
def add_card(card_name, quantity, from_set, price):
	hash_id = generate_hash(card_name, from_set)

	# Checks if card exists, if it does it increments the value, if not, it creates the card and then increments the value by the quantity.
	card = cursor.execute('SELECT card_name FROM card_inventory WHERE hash_id = ?', [hash_id]).fetchone()

	if card is None:
		cursor.execute('INSERT INTO card_inventory VALUES (?, ?, ?, ?, ?)', [card_name, quantity, from_set, price, hash_id])
	
	else:
		cursor.execute('UPDATE card_inventory SET quantity = quantity + ? WHERE hash_id = ?', [quantity, hash_id])

	update_db('Added {} {} from set {} at price {}.'.format(quantity, card_name, from_set, price))

# Removes a card from the inventory DB.
def remove_card(card_name, quantity, from_set):
	hash_id = generate_hash(card_name, from_set) 

	qty = cursor.execute('SELECT quantity FROM card_inventory WHERE hash_id = ?', [hash_id]).fetchone()	

	if qty is not None and qty[0] > quantity:
		cursor.execute('UPDATE card_inventory SET quantity = quantity - ? WHERE hash_id = ?', [quantity, hash_id])

	update_db('Removed {} {} from set {}.'.format(quantity, card_name, from_set))

def main():
	add_card('Reliquary Tower', 2, 'Core Set 2019', 2.49)
	add_card('Reliquary Tower', 2, 'Commander 2016', 2.49)
	add_card('Reliquary Tower', 2, 'PM19', 2.49)

if __name__ == '__main__':
	main()
