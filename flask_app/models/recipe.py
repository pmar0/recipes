from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Recipe:
    db = "recipe_schema"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.date_made = db_data['date_made']
        self.under_30 = db_data['under_30']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        recipes_from_db = connectToMySQL(Recipe.db).query_db(query)
        recipes = []
    
        for recipe in recipes_from_db:
            recipes.append(cls(recipe))
    
        return recipes
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        recipe = connectToMySQL(Recipe.db).query_db(query,data)
        if recipe:
            return cls(recipe[0])
        return False

    @classmethod
    def save(cls, form_data):
        query = 'INSERT INTO recipes (name,description,instructions,date_made,under_30,user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30)s,%(user_id)s);'
        return connectToMySQL(Recipe.db).query_db(query,form_data)

    @classmethod
    def update(cls,form_data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s , date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;'
        return connectToMySQL(Recipe.db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(Recipe.db).query_db(query,data)
    
    @staticmethod
    def validate_recipe(form_data):
        valid = True

        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters long.","name")
            valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long.","description")
            valid = False
        if len(form_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.","instructions")
            valid = False
        try:
            if (datetime.today() < datetime.strptime(form_data['date_made'],'%Y-%m-%d')):
                flash("Tell me your secrets.","date_made")
                valid = False
        except Exception:
            flash("Please input a valid date.", "date_made")
            valid = False
        if 'under_30' not in form_data:
            flash("Give me cook time.","under_30")
            valid = False

        return valid