from recipes_app.config.mysqlconnection import connectToMySQL
from recipes_app import DATABASE
from flask import flash, session
from recipes_app.models.user_model import User


class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.under_30 = data["under_30"]
        self.date_made = data["date_made"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"

        results = connectToMySQL(DATABASE).query_db(query)

        recipes = []

        if results:
            for dict in results:
                new_user = cls(dict)
                recipes.append(new_user)

        return recipes

    @classmethod
    def get_all_with_user(cls):
        query = """
        
        SELECT * FROM recipes
        JOIN users ON 
        recipes.user_id = users.id;
        
        """

        results = connectToMySQL(DATABASE).query_db(query)

        recipes = []

        if results:
            for row in results:
                recipe = cls(row)

                user_data = {
                    **row,
                    "id": row["users.id"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                }

                user = User(user_data)

                recipe.creator = user

                recipes.append(recipe)

        return recipes

    @classmethod
    def get_one(cls, id):
        data = {
            "id": id,
        }

        query = """
            SELECT * FROM recipes
            WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        recipe = cls(results[0])

        return recipe

    @classmethod
    def save(cls, data):
        query = """
        
        UPDATE recipes
        SET
        name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s,
        under_30 = %(under_30)s,
        date_made = %(date_made)s
        WHERE
        id = %(id)s;
        
        """

        connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def create(cls, form):
        data = {**form, "user_id": session["uid"]}

        query = "INSERT INTO recipes (name, description, instructions, under_30, date_made, user_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(user_id)s)"

        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(form):
        is_valid = True

        if len(form["name"]) < 3:
            is_valid = False
            flash("Too short!")
        if len(form["description"]) < 3:
            is_valid = False
            flash("Please add description!")
        if len(form["instructions"]) < 3:
            is_valid = False
            flash("Please add instructions!")

        return is_valid

    @classmethod
    def delete(cls, id):
        data = {
            "id": id,
        }

        query = """
        
        DELETE FROM recipes
        WHERE id = %(id)s;
        
        """
        connectToMySQL(DATABASE).query_db(query, data)
