from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    session['logged_in'] = False
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'password_conf' : request.form['password_conf'],
        'unhashed_pw' : request.form['password']
    }
    if not User.validate(data):
        session['reg_attempt'] = True
        return redirect('/')
    User.create(data)
    user = User.retrieve_via_email(data)
    session['logged_in'] = True
    session['user_id'] = user.id
    return redirect('/recipes')

@app.route('/recipes')
def recipes():
    if session['logged_in'] == True:
            user= User.retrieve_via_id(session['user_id'])
            recipes = Recipe.get_all()
            return render_template('recipes.html', user = user, recipes = recipes)
    session['bad_egg'] = True
    flash('You must be logged in to view recipes')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {'email' : request.form['email']}
    user = User.retrieve_via_email(data)
    if user == False or not bcrypt.check_password_hash(user.password, request.form['password']):
        session['login_attempt'] = True
        flash('Invalid password/email combo')
        return redirect('/')
    session['logged_in'] = True
    session['user_id'] = user.id
    return redirect('/recipes')


