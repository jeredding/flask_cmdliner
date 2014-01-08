# WRITTEN FOR PYTHON3
### CMDLINER: the REST interface for command-line calls!

import sqlite3
import locale
from subprocess import check_output, CalledProcessError
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing


DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
DATABASE = 'cmds.db'
PASSWORD = 'default'

#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# app.logger.debug('A value for debugging')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')


# Create the app!
app = Flask(__name__)
app.config.from_object(__name__)


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('cmdliner.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def execute_cmd(cmd):
    """
        run a command, return the code and the body
    """
    encoding = locale.getdefaultlocale()[1]
    try:
        output = check_output(cmd, shell=True)
    except CalledProcessError as e:
        return (e.returncode, e.output)
    else:
        return (0, output.decode(encoding).split('\n'))


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_cmds'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_cmds'))


@app.route('/cmd/<int:cmd_id>/run', methods=['POST'])
def run_cmd(cmd_id):
    if not session.get('logged_in'):
        abort(401)
    entries = list_cmds()
    cmd = list(filter(lambda t: t['id'] == cmd_id, entries))
    # if len(cmd) == 0:
    #     abort(404)
    xit_code, output = execute_cmd(cmd[0])
    flash("result: %d\n output: %s" % (xit_code, output))
    return redirect(url_for('show_cmds'))


@app.route('/cmd', methods=['POST'])
def add_cmd():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into cmds (title, command) values (?, ?)',
                 [request.form['title'], request.form['command']])
    g.db.commit()
    flash('New entry was successfully posted: %s -> %s' %
          (request.form['title'], request.form['command']))
    return redirect(url_for('show_cmds'))


@app.route('/cmd/<int:cmd_id>', methods=['DELETE'])
def rm_cmd(cmd_id):
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('delete from cmds where id =  ?',
                 [request.form['cmd_id']])
    g.db.commit()
    flash('Entry was removed successfully %s -> %s' %
          (request.form['title'], request.form['command']))
    return redirect(url_for('show_cmds'))


@app.route('/')
def show_cmds():
    entries = list_cmds()
    return render_template('show_cmds.html', cmds=entries)


def list_cmds():
    cur = g.db.execute('select id, title, command from cmds order by id desc')
    entries = {}
    for row in cur.fetchall():
        entries[row[0]] = {'title': row[1], 'command': row[2]}
    print (entries)
    return entries

if __name__ == '__main__':
    app.run()
