import sqlite3

# connect and open the database file database.db
conn = sqlite3.connect('database.db')
print ("Opened database successfully")

# use the opened connection to read all cards into a cursor
cursorCard = conn.execute("SELECT cardid, title from card")
cursorStaff = conn.execute("SELECT staffid,fullName,email,github FROM staff")
# loop over all rows in the cursorCard and print the cardid and title column
for row in cursorCard:
   print ("CARDID = ", row[0], "TITLE = ", row[1] )
#loop over all rows in cursor staff
for row in cursorStaff:
    print("STAFFID =", row[0], "NAME =", row[1], "EMAIL =", row[2], "GITHUB =", row[3])
# close the connection
print ("Operation done successfully")
conn.close()
