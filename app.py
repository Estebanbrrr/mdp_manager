
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint

from controllers.auth_security import *
from controllers.client_manager import *


app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



@app.route('/')
def show_accueil():
    return render_template('auth/layout.html')

@app.before_request
def before_request():
     if request.path.startswith('/admin') or request.path.startswith('/client'):
        if 'role' not in session:
            return redirect('/login')
        else:
            if (request.path.startswith('/client') and session['role'] != 'ROLE_client') or (request.path.startswith('/admin') and session['role'] != 'ROLE_admin'):
                print('pb de route : ', session['role'], request.path.title(), ' => deconnexion')
                session.pop('login', None)
                session.pop('role', None)
                return redirect('/login')


app.register_blueprint(auth_security)
app.register_blueprint(client_manager)

if __name__ == '__main__':
    app.run()
