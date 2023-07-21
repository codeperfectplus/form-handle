import flask
import sqlite3

# it can be hashed and saved to db as well
check_password = 'password'

# create app
connector = sqlite3.connect('database.db', check_same_thread=False)
cursor = connector.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS contact (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT, source TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS newsletter (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, source TEXT)')
connector.commit()

app = flask.Flask(__name__)

@app.route('/contact', methods=['POST'])
def contact_us():
    # get post data
    data = flask.request.form
    name = data['name']
    email = data['_replyto']
    message = data['message']
    source = data['source']

    cursor.execute('INSERT INTO contact (name, email, message, source) VALUES (?, ?, ?, ?)', (name, email, message, source))
    connector.commit()
    return flask.redirect(source)

@app.route('/newsletter', methods=['POST'])
def newsletter():
    # get post data
    data = flask.request.form
    email = data['email']
    source = data['source']

    cursor.execute('INSERT INTO newsletter (email, source) VALUES (?, ?)', (email, source))
    connector.commit()
    return flask.redirect(source)


@app.route('/', methods=['GET'])
def index():
    return flask.jsonify({'status': 'ok'})


# get contact and newsletter data from database with password
@app.route('/data', methods=['GET'])
def data():
    # get password
    password = flask.request.args.get('password')
    if password != check_password:
        return flask.jsonify({'status': 'error', 'message': 'wrong password'})

    # get data
    cursor.execute('SELECT * FROM contact')
    contact = cursor.fetchall()
    cursor.execute('SELECT * FROM newsletter')
    newsletter = cursor.fetchall()
    return flask.jsonify({'status': 'ok', 'contact': contact, 'newsletter': newsletter})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
