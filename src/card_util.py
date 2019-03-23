import json 
import requests

scryfall_fuzzy_card_search = 'https://api.scryfall.com/cards/named?fuzzy='

codes = {} # [English Text Set Name] -> Code
texts = {} # [Code] -> English Text Set Name

# Load the MTG set codes into memory.
with open('./sets.dsv', 'r') as DSV:
	for line in DSV:
		' '.join(line.split())
		values = line.split()

		code = values[0]
		full_text = ' '.join(values[1:len(values)])

		codes[full_text.lower()] = code
		texts[code.lower()] = full_text

# Just a class for holding card data from Scryfall. 
class Card:
	def __init__(self, name, card_type, mana_cost, from_set_code, from_set, oracle_text, collector_number, prices, legality, card_images):
		self.name = name
		self.card_type = card_type
		self.mana_cost = mana_cost
		self.from_set_code = from_set_code
		self.from_set = from_set
		self.oracle_text = oracle_text
		self.collector_number = collector_number
		self.prices = prices
		self.legality = legality
		self.card_images = card_images

	def display_card(self):
		print('[' + self.name + ']')
		print('Card Type: ' + self.card_type)
		print('Mana Cost: ' + self.mana_cost)
		print('Set Code: ' + self.from_set_code)
		print('Set Name: ' + self.from_set)
		print('Oracle Text: ' + self.oracle_text)
		print('Collector Number: ' + self.collector_number)
		print(self.prices)
		print(self.legality)
		print(self.card_images)

# generate_card_from_name ... Instantiates a Card with the values gotten from Scryfall if there is an error with the req, it returns None.
def generate_card_from_name(name):
	req = requests.get(scryfall_fuzzy_card_search + name)
	req_obj = req.json() 

	if req_obj['object'] == 'error':
		return None

	else:
		name = req_obj['name']
		card_type = req_obj['type_line']
		mana_cost = req_obj['mana_cost']
		from_set_code = req_obj['set']
		from_set = req_obj['set']
		oracle_text = req_obj['oracle_text']
		collector_number = req_obj['collector_number']
		prices = req_obj['prices']
		legality = req_obj['legalities']
		card_images = req_obj['image_uris']

		return Card(name, card_type, mana_cost, from_set_code, from_set, collector_number, oracle_text, prices, legality, card_images)

# get_set_from_name ... Generates a card and returns the set name.
def get_set_from_name(name):
	card = generate_card_from_name(name)
	return card.from_set

# to_code ... Converts a set name to a set code. Returns None if fail-to-find.
def to_code(from_set):
	return codes.get(from_set, None)

# to_set ... Converts a set code to a set name. Returns None if fail-to-find.
def to_set(set_code):
	return texts.get(set_code, None)
