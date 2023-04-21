from flask import flash
from recipes_app.config.mysqlconnection import connectToMySQL


from recipes_app import DATABASE, BCRYPT

import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_one(cls, id):
        data = {"id": id}

        query = "SELECT * FROM users WHERE id = %(id)s;"

        return cls(connectToMySQL(DATABASE).query_db(query, data)[0])

    @classmethod
    def register(cls, form):
        hash = BCRYPT.generate_password_hash(form["password"])

        form = {
            **form,
            "password": hash,
        }

        query = """
        
            INSERT INTO users
            (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        
        """

        return connectToMySQL(DATABASE).query_db(query, form)

    @classmethod
    def get_one_by_email(cls, email):
        data = {"email": email}

        query = """
        
        SELECT * FROM users
        WHERE
        email = %(email)s;
        
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False

    @classmethod
    def validate_login(cls, form):
        found_user = cls.get_one_by_email(form["email"])

        if found_user:
            if BCRYPT.check_password_hash(found_user.password, form["password"]):
                return found_user

            else:
                flash("Invalid Password")
                return False

        else:
            flash("Invalid Login")
            return False

    @classmethod
    def validate(cls, form):
        is_valid = True

        if len(form["first_name"]) < 2:
            flash("First name too short!")
            is_valid = False

        if len(form["last_name"]) < 2:
            flash("Last name too short!")
            is_valid = False

        if not EMAIL_REGEX.match(form["email"]):
            flash("Invalid email!")
            is_valid = False

        elif cls.get_one_by_email(form["email"]):
            flash("Email already registered!")
            is_valid = False

        if len(form["password"]) < 5:
            flash("Password too short!")
            is_valid = False

        if not re.search("[A-Z]", form["password"]):
            flash("Password must contain at least one uppercase letter.")
            is_valid = False

        if not re.search("[0-9]", form["password"]):
            flash("Password must contain one number.")

        if form["password"] != form["confirm_password"]:
            flash("Password must match!")
            is_valid = False

        
        
        return is_valid

    # @classmethod
    # def get_one_with_recipes(cls, id):
    #     data = {
    #         "id": id,
    #     }

    #     query = """
        
    #     SELECT * FROM users
    #     LEFT JOIN recipes ON 
    #     users.id = recipes.user_id
    #     WHERE users.id = %(id)s;
        
    #     """

    #     results = connectToMySQL(DATABASE).query_db(query, data)

    #     recipes = []

    #     user = cls(results[0])
    #     if results:
    #         for row in results:
    #             recipe_data = {
    #                 "id": row["users.id"],
    #                 "name": row["name"],
    #                 "description": row["description"],
    #                 "instruction": row["instruction"],
    #                 "created_at": row["created_at"],
    #                 "updated_at": row["updated_at"],
    #                 "user_id": row["user_id"],
    #             }

    #             recipe = Recipe(recipe_data)

    #             recipes.append(recipe)

    #         user.recipes = recipes

    #     return user
