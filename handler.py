import flask
import sqlite3

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


if __name__ == '__main__':
    app.run()
