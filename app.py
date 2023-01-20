from flask import Flask, render_template, redirect, request, make_response
import sqlite3
import security

app = Flask(__name__)

connection = sqlite3.connect('cashco.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users (username text, password text, balance int)')
cursor.execute('CREATE TABLE IF NOT EXISTS msg (feature int, receiver text, cnt text)')

connection.commit()
connection.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    connection = sqlite3.connect('cashco.db')
    cursor = connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login = security.login(username, password)

        if login['user_exists']:
            if login['auth']:
                response = make_response('You are logged in to your account. Click <a href="/">here</a>.')
                response.set_cookie('cashco_user', username)
                return response
            else:
                return 'Error: Incorrect password'

        cursor.execute('INSERT INTO users (username, password, balance) VALUES (?, ?, 5000)', (username, password))
        connection.commit()
        response = make_response('Your new account has been created. Click <a href="/">here</a> to access CashCo.')
        response.set_cookie('cashco_user', username)
        return response

    print(request.cookies.get('cashco_user'))

    connection.commit()
    
    if len(list(cursor.execute('SELECT * FROM users WHERE username=?', (request.cookies.get('cashco_user'),)))) > 0:
        return render_template('index.html', user=request.cookies.get('cashco_user'))
    
    return render_template('login.html')

@app.route('/signout')
def signout():
    response = make_response(f'You are signed out from your previous account ({request.cookies.get("cashco_user")}). Click <a href="/">here</a> to log on from another account.')
    response.set_cookie('cashco_user', '')
    return response

@app.route('/msg')
def msg():
    connection = sqlite3.connect('cashco.db')
    cursor = connection.cursor()
    
    if len(list(cursor.execute('SELECT * FROM users WHERE username=?', (request.cookies.get('cashco_user'),)))) > 0:
        all_msg = list(cursor.execute('SELECT * FROM msg WHERE receiver=?', ((request.cookies.get('cashco_user')),)))
        return render_template('msg.html', all_msg=all_msg, len=len)

    connection.close()
    
    return redirect('http://127.0.0.1:5000')

app.run(debug=True, port='5000')