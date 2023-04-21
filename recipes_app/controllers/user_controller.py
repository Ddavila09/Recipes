from recipes_app import app
from flask import render_template, request, redirect, session
from recipes_app.models.user_model import User
from recipes_app.controllers.recipe_controller import Recipe
from recipes_app.models.recipe_model import Recipe






@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_user', methods=['POST'])
def new_user():
        
    if not User.validate(request.form):
        print('hello')
        return redirect('/')
        
    
    found_user=User.register(request.form)
    
    if found_user:
        session['uid'] = found_user
    return redirect('/dashboard')



@app.route('/login', methods=['POST'])
def login():
    
    
    
    found_user = User.validate_login(request.form)
    
    if found_user:
        
        session['uid'] = found_user.id
        
        
        return redirect('/dashboard')
    else:
        return redirect('/')
    
    

@app.route('/dashboard')
def dashboard():
    
    if 'uid' not in session:
        return redirect('/')
    
    recipes=Recipe.get_all_with_user()
    
    return render_template("dashboard.html", user = User.get_one(session['uid']), recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')