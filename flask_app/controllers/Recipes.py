from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.recipe import Recipe

@app.route('/recipes/new')
def create_recipe():
    if 'user_id' not in session:
        return redirect('index.html')
    return render_template('recipe_new.html')

@app.route('/recipes/process', methods=['POST'])
def process_recipe():
    if 'user_id' not in session:
        return redirect('/user/login')

    if Recipe.validate_recipe(request.form):
        data = {
            'user_id': session['user_id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_made': request.form['date_made'],
            'under_30': request.form['under_30'],
        }
        Recipe.save(data)
        return redirect('/dashboard')
    return redirect('/recipes/new')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('recipe_view.html',recipe=Recipe.get_by_id({'id': id}))

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('recipe_edit.html',recipe=Recipe.get_by_id({'id': id}))

@app.route('/recipes/edit/<int:id>/process', methods=['POST'])
def process_edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    if Recipe.validate_recipe(request.form):
        data = {
            'id': id,
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_made': request.form['date_made'],
            'under_30': request.form['under_30'],
        }
        Recipe.update(data)
        return redirect('/dashboard')

    return redirect(f'/recipes/edit/{id}')

@app.route('/recipes/destroy/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Recipe.destroy({'id':id})
    return redirect('/dashboard')
