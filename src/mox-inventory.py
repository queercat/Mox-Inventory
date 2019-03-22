#!/usr/local/bin/python3
# Mox Inventory -- A Scryfall powered opensource MTG invetory utility.

import json # Handles JSON data.
import sqlite3 # Backend DB for MOXI.
import card # A utility for creating and handling magic cards.
import requests # Handles even more web reqs.
import flask # Awesome microservice for handling web reqs.
import hashlib # Creating hashes for card IDs.

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

# Removes a card from the inventory DB adds it to the invoice list if money was made.
def remove_card(card_name, quantity, from_set, sell_price):
	hash_id = generate_hash(card_name, from_set) 

	qty = cursor.execute('SELECT quantity FROM card_inventory WHERE hash_id = ?', [hash_id]).fetchone()	

	if qty is not None and qty[0] > quantity:
		cursor.execute('UPDATE card_inventory SET quantity = quantity - ? WHERE hash_id = ?', [quantity, hash_id])

		update_db('Removed {} {} from set {}.'.format(quantity, card_name, from_set))

		if sell_price > 0:
			card = cursor.execute('SELECT card_name FROM invoice_list WHERE hash_id = ? AND sell_price = ?', [hash_id, sell_price])
		
			if card is not None:
				cursor.execute('UPDATE invoice_list SET quantity = quantity + ? WHERE hash_id = ? AND sell_price = ?', [quantity, hash_id, sell_price])

			else:
				cursor.execute('INSERT INTO invoice_list VALUES (?, ?, ?, ?, ?)', [card_name, quantity, from_set, sell_price, hash_id])

			update_db('Sold {} {} from set {} for {}.'.format(quantity, card_name, from_set, sell_price))

app = flask.Flask(__name__)

@app.route('/cards/<uuid>', methods = ['POST'])
def handle_add():
	message = flask.request.json
	
	token = message['token'] # Some private token IDK.
	additions = message['additions'] # Additions are going to be raising the quantity of a card.
	removals = message['removals'] # Removals are going to be lowering the quantity of a card.

	for card in additions:
		card_name = card['card_name']
		quantity = card['quantity']
		from_set = card['from_set']
		price = card['price']	

		add_card(card_name, quantity, from_set, price)

	for card in removals:
		card_name = card['card_name']
		quantity = card['quantity']
		from_set = card['from_set']
		sell_price = card['sell_price']	

		remove_card(card_name, quantity, from_set, sell_price) 


def main():

if __name__ == '__main__':
	main()
