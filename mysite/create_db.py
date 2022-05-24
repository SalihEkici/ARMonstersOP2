# import the sqlite3 library to work with SQLite databases in Python
import sqlite3

# connect and open the database file database.db, the database will be created when it does not exists
conn = sqlite3.connect('database.db')
print("Opened database successfully")

# create a new table card with two columns:
# the first column cardid is the primary key and autoincrement
# the second column contains the card title
conn.execute('CREATE TABLE card (cardid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT)')
print("Table card created successfully")

# insert four rows in the newly created table
conn.execute("INSERT INTO card (title) VALUES ('Happy birthday')")
conn.execute("INSERT INTO card (title) VALUES ('A very big thank you')")
conn.execute("INSERT INTO card (title) VALUES ('Graduation party')")
conn.execute("INSERT INTO card (title) VALUES ('Happy Retirement')")
print("Cards inserted successfully")

# create a second table wish with four columns:
# the first column wishid is the primary key and autoincrement
# the second column contains the sender of the wishes
# the third column contains the message from the sender
# the fourth column contains the id of the card
conn.execute('CREATE TABLE wish (wishid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, sender TEXT, message TEXT, cardid INTEGER, receiver TEXT)')
# there are no wishes already sent, so the table stays empty
print("Table wish created successfully")

conn.execute("CREATE TABLE staff (staffid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, fullName TEXT, email TEXT, github TEXT)")
conn.execute('INSERT INTO staff (fullName,email,github) VALUES("Salih Ekici","r0883622@student.thomasmore.be","https://github.com/SalihEkici")')
conn.execute('INSERT INTO staff (fullName,email,github) VALUES("Kyano Trevisan","r0894962@student.thomasmore.be","https://github.com/kyanoTrevisan/")')
# commit all changes to the database, otherwise they will be lost
conn.commit()

# close the connection
conn.close()
