# A very simple Flask Hello World app for you to get started with...
import code
import key
from flask import Flask,render_template, jsonify, request
import requests
import sqlite3
import string
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/cards')
def list_cards():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cards = cur.execute('SELECT * FROM card;').fetchall()
    conn.close()
    return render_template('cards.html', cards=cards)

@app.route('/wish')
def wish_form():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cards = cur.execute('SELECT * FROM card;').fetchall()
    conn.close()
    return render_template('form_wish.html', cards=cards)

@app.route('/wish_list')
def wish_list():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    wishes = cur.execute('SELECT * FROM wish').fetchall()
    conn.close()
    return render_template('wish_list.html', wishes = wishes)

@app.route('/wish_insert', methods=['POST'])
def wish_insert():
    S = 8  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    random_access_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    sender = request.form.get("sender")
    message = request.form.get("message")
    cardid = request.form.get("cardid")
    receiver = request.form.get("receiver")
    receiver_email = request.form.get("receiver_email")
    giftMethod = request.form.get("giftMethod")
    # connect and open the database file database.db
    conn = sqlite3.connect('database.db')
    conn.execute(f"INSERT INTO wish (cardid,sender,receiver,message,code) VALUES ('{cardid}','{sender}', '{receiver}', '{message}','{random_access_code}')")
    # commit the new row to the database, otherwise it will be lost
    conn.commit()
    conn.row_factory = dict_factory
    cur = conn.cursor()
    image = cur.execute("SELECT title from card where cardid = '" + cardid + "'").fetchone()
    
    #send email with data from form
    if(giftMethod == "2"): 
        requests.post(
            "https://api.mailgun.net/v3/sandbox6f8b2699467b4c70822f3693c7ac5877.mailgun.org/messages",
            auth=("api", "5d0ae248efa80711e3d556146a12376d-8d821f0c-4fc5a289"),
            data={"from": "salih@ARMonsters.mailgun.com",
            "to": f"{receiver_email}",
            "subject": "You have received a greeting card from " + sender ,
            "text": message + "\nAccess code = " + random_access_code})
        return render_template('wish_confirmation.html')
    else:
        
        
        # close the connection
        conn.close()
        print(message)
        print(image)
        return render_template('print_wish.html', message = message, image = image)
    
    

@app.route('/staff')
def staff_list():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    staff_list = cur.execute('SELECT * FROM staff').fetchall()
    conn.commit()
    conn.close()
    return render_template('staff.html', staff_list = staff_list)

@app.route('/unique_code')
def unique_code():
    return render_template('unique_code.html')

@app.route('/get_card', methods=['POST'])
def show_message():
    unique_code = request.form.get("code")
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    message = cur.execute("SELECT message from wish where code = '" + unique_code + "'").fetchone()
    sender = cur.execute("SELECT sender from wish where code = '" + unique_code + "'").fetchone()
    conn.commit()
    print(message)
    print(unique_code)
    if message == None:
        return render_template("error.html") 
    conn.close()    
    return render_template("message.html", unique_code = unique_code, message = message,sender = sender)
if __name__ == "__main__":
    app.run(debug=True)