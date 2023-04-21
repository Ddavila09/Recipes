from flask import  render_template, request, redirect, session

from recipes_app.models.recipe_model import Recipe
from recipes_app.models.user_model import User
from recipes_app.controllers.user_controller import User
from flask import flash
from recipes_app import app


app.secret_key = "poggers"



@app.route('/recipe/new')
def new_recipe():
    
    if 'uid' not in session:
        return redirect('/')
    
    
    return render_template("new_recipe.html",  recipes=Recipe.get_all())


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    
    
    if Recipe.validate(request.form):
        Recipe.create(request.form)
        return redirect('/dashboard')
    else:    
        return redirect('/recipe/new')
    



@app.route('/edit_recipe/<int:id>')
def edit_user(id):
    # print(id)
    Recipe.get_one(id)
    return render_template('edit_recipe.html', recipe=Recipe.get_one(id))


@app.route('/save_recipe', methods=['POST'])
def save_recipe():
    
    if not Recipe.validate(request.form):
        return redirect(f'/edit_recipe/{request.form["id"]}')
        
    Recipe.save(request.form)
    return redirect('/dashboard')
    
    
@app.route('/show_recipe/<int:id>')
def show_recipe(id):
    recipe = Recipe.get_one(id)
    user_id = session['uid']
    user = User.get_one(user_id)
    created = User.get_one(recipe.user_id)
    return render_template('show_recipe.html', recipe=recipe, user=user, created=created)
    
    


@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):
    
    Recipe.delete(id)
    
    return redirect('/dashboard')












@app.route('/reset_session')
def reset():
    session.clear()
    return redirect('/')
