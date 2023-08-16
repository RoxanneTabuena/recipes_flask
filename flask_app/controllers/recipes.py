from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/create', methods=['POST'])
def create():
    data = {
        'name' : request.form['name'],
        'under_30' : request.form['under_30'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'user_id' : session['user_id']
    }
    if not Recipe.validate(data):
        return redirect('/new')
    Recipe.create(data)
    return redirect('/recipes')

@app.route('/view/<int:id>')
def view(id):
    if not session['logged_in']:
            session['bad_egg'] = True
            flash('You must be logged in to view recipes')
            return redirect('/')
    user = User.retrieve_via_id(session['user_id'])
    recipe = Recipe.get_one(id)
    return render_template('view.html', recipe=recipe, user=user)

@app.route('/edit/<int:id>')
def edit(id):
    recipe = Recipe.get_one(id)
    if not session['logged_in']:
        session['bad_egg'] = True
        flash('You must be logged in to edit recipes')
        return redirect('/')
    if recipe.creator.id != session['user_id']:
        session['bad_egg'] = True
        flash('That is not your recipe to edit, you have been logged out')
        session['logged_in'] = False
        return redirect('/')
    return render_template('edit.html', recipe=recipe)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    recipe = Recipe.get_one(id)
    data = {
    'id' : id,
    'name' : request.form['name'],
    'under_30' : request.form['under_30'],
    'description' : request.form['description'],
    'instructions' : request.form['instructions'],
    'date_made' : request.form['date_made'],
    }
    if request.form[f'name'] == '':
        data['name'] = recipe.name
    if request.form[f'under_30'] == '':
        data['under_30'] = recipe.under_30
    if request.form[f'description'] == '':
        data['description'] = recipe.description
    if request.form[f'instructions'] == '':
        data['instructions'] = recipe.instructions
    if request.form[f'date_made'] == '':
        data['date_made'] = recipe.date_made
    Recipe.update(data)
    return redirect('/view/'+str(id))

@app.route('/delete/<int:id>')
def delete(id):
    if not session['logged_in']:
        session['bad_egg'] = True
        flash('You must be logged in to delete recipes')
        return redirect('/')
    data = {'id' : id}
    Recipe.delete(data)
    return redirect('/recipes')