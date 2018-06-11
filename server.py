import re, bcrypt, json
from flask import Flask, session, request, redirect, render_template, flash, url_for
from db.data_layer import get_request, get_user_by_email, get_user_by_id, create_user, search_movie, create_like, delete_like, get_user_like
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = '8118d0875ad5b6b3ad830b956b111fb0'
csrf = CSRFProtect(app)

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

def is_blank(name, field):
    if len(field) == 0:
        flash('{} cannot be blank'.format(name))
        return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate')
def authenticate():
    return render_template('authenticate.html')

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['html_fullname']
    email = request.form['html_email']
    password = request.form['html_password']
    confirm = request.form['html_confirm']

    is_valid = True

    is_valid = not is_blank('fullname', fullname)
    is_valid = not is_blank('email', email)
    is_valid = not is_blank('password', password)
    is_valid = not is_blank('confirm', confirm)

    if password != confirm:
        flash('password not match')
        is_valid = False
    if len(password) < 6:
        flash('pass to short')
    if not EMAIL_REGEX.match(email):
        flash('email is not right format')
    
    if is_valid:
        try:
            encoded = password.encode('UTF-8')
            encrypted = bcrypt.hashpw(encoded, bcrypt.gensalt())
            user = create_user(email, fullname, encrypted)
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('index'))
        except:
            flash('email already registered dude')
    
    return redirect(url_for('authenticate'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['html_email']
    password = request.form['html_password']

    try:
        user = get_user_by_email(email)
        
        encoded = password.encode('UTF-8')
        if bcrypt.checkpw(encoded, user.password):
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('index'))
        else:
            flash('Password not match')
    except:
        flash('Invalid login')

    return redirect(url_for('authenticate'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search_query():
    query = request.form['query']
    return redirect(url_for('search', query=query))

@app.route('/search/<query>')
def search(query):
    movies = search_movie(query)
    return render_template('search.html', movies=movies)

@app.route('/like/<movie_id>')
def create_user_like(movie_id):
    user = get_user_by_id(session['user_id'])
    create_like(user.id, movie_id)
    return redirect(url_for('get_like', user_id=user.id))

@app.route('/unlike/<movie_id>')
def delete_user_like(movie_id):
    user = get_user_by_id(session['user_id'])
    delete_like(movie_id)
    return redirect(url_for('get_like', user_id=user.id))

@app.route('/user/<user_id>')
def get_like(user_id):
    user = get_user_by_id(user_id)
    movies = get_user_like(user.id)
    return render_template('like.html', movies=movies)

app.jinja_env.auto_reload = True
app.config['TEMPLATE_AUTO_RELOAD'] = True

app.run(debug=True, use_reloader=True)