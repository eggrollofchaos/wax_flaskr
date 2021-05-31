import sqlite3
from pathlib import Path

from flask import Flask, g, render_template, request, session, \
    flash, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

basedir = Path(__file__).resolve().parent

# configuration
DATABASE = "flaskr.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "change_me"
SQLALCHEMY_DATABASE_URI = f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# create and initialize a new Flask app
app = Flask(__name__)
# load the config
app.config.from_object(__name__)
# init sqlalchemy
db = SQLAlchemy(app)

from project import models

# connect to database
# def connect_db():
#     """Connects to the database."""
#     rv = sqlite3.connect(app.config["DATABASE"])
#     rv.row_factory = sqlite3.Row
#     return rv


# create the database
# def init_db():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource("schema.sql", mode="r") as f:
#             db.cursor().executescript(f.read())
#             db.commit()


# open database connection
# def get_db():
#     if not hasattr(g, "sqlite_db"):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db


# close database connection
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g,  "sqlite_db"):
#         g.sqlite_db.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to database."""
    if not session.get('logged_in'):
        abort(401)
    # db = get_db()
    new_entry = models.Post(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    # db.execute(
    #     'insert into entries (title, text) values (?, ?)',
    #     [request.form['title'], request.form['text']]
    # )
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/delete/<post_id>', methods=['GET'])
def delete_entry(post_id):
    """Delete post from database"""
    result = {'status': 0, 'message': 'Error'}
    try:
        # db = get_db()
        # db.execute('delete from entries where id=' + post_id)
        # db.commit()
        db.session.query(models.Post).filter_by(id=post_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return jsonify(result)


@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get("query")
    entries = db.session.query(models.Post)
    if query:
        return render_template('search.html', entries=entries, query=query)
    return render_template('search.html')

@app.route('/')
# def hello():
def index():
    """Searches the database for entries, then displays them."""
    # db = get_db()
    # cur = db.execute('select * from entries order by id desc')
    # entries = cur.fetchall()
    entries = db.session.query(models.Post)
    return render_template('index.html', entries=entries)
    # return "Hello, World!"


if __name__ == "__main__":
    app.run()
