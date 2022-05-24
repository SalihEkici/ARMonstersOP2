# A very simple Flask Hello World app for you to get started with...
import key
from flask import Flask,render_template, jsonify, request
import requests
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    sender = request.form.get("sender")
    message = request.form.get("message")
    cardid = request.form.get("cardid")
    receiver = request.form.get("receiver")
    receiver_email = request.form.get("receiver_email")
    giftMethod = request.form.get("giftMethod")
    # connect and open the database file database.db
    conn = sqlite3.connect('database.db')
    conn.execute(f"INSERT INTO wish (cardid,sender,receiver,message) VALUES ('{cardid}','{sender}', '{receiver}', '{message}')")
    # commit the new row to the database, otherwise it will be lost
    conn.commit()
    # close the connection
    conn.close()
    if(giftMethod == "Email"):
        requests.post(
            "https://api.mailgun.net/v3/sandbox784cba45b781488ba33c9e360d748f81.mailgun.org/messages",
            auth=("api", key.API),
            data={"from": "ARMonster@armonster.com",
                "to": receiver_email,
                "subject": "Hello",
                "text": message})
            
    return render_template('wish_confirmation.html')

@app.route('/staff')
def staff_list():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    staff_list = cur.execute('SELECT * FROM staff').fetchall()
    conn.commit()
    conn.close()
    return render_template('staff.html', staff_list = staff_list)


if __name__ == "__main__":
    app.run(debug=True)