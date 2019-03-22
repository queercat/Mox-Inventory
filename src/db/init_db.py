import sqlite3

def create_db():
	conn = sqlite3.connect('./inventory.db')
	return conn, conn.cursor()		

def create_tables(conn, cursor):
	cursor.execute('CREATE TABLE card_inventory (card_name text, quantity int, from_set text, price text, hash_id text)') 
	cursor.execute('CREATE TABLE db_interactions (interaction text)')
	conn.commit()

def main():
	conn, cursor = create_db()
	create_tables(conn, cursor)

if __name__ == '__main__':
	main()
