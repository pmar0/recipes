from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.errorhandler(404)
def error(e):
    return redirect('/user/login')

@app.route('/user/login/')
def login():
    if 'user_id' not in session:
        return render_template('index.html')
    return redirect('/dashboard')

@app.route('/user/login/process', methods=['POST'])
def login_success():
    user = User.validate_login(request.form)

    if user:
        session['user_id'] = user.id
        return redirect('/dashboard')
    
    return redirect('/user/login')

@app.route('/user/register/process', methods=['POST'])
def register_success():
    if not User.validate_reg(request.form):
        return redirect('/user/login')
    user_id = User.save(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/dashboard/')
def dashboard():
    if 'user_id' in session:
        user = User.get_by_id({"id":session['user_id']})
        if user:
            return render_template('dashboard.html', user=user, recipes=Recipe.get_all())
    return redirect('/user/login')

@app.route('/user/logout/')
def logout():
    if 'user_id' in session:
        session.clear()
    return redirect('/user/login')