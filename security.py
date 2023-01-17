import sqlite3

def login(name, password):
    connection = sqlite3.connect('cashco.db')
    cursor = connection.cursor()

    user_exists = len(list(cursor.execute('SELECT * FROM users WHERE username=?', (name,)))) == 1

    if user_exists:
        user = (list(cursor.execute('SELECT * FROM users WHERE username=?', (name,))))[0]

        if user[1] == password:
            auth = True
        else:
            auth = False

    else:
        auth = False

    return {'user_exists': user_exists, 'auth': auth}