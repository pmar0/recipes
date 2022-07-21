from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re

class User:
    db = "recipe_schema"

    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,form_data):
        hashed_data = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': bcrypt.generate_password_hash(form_data['password']),
        }
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        user_id = connectToMySQL(User.db).query_db(query,hashed_data)
        return user_id

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        if connectToMySQL(User.db).query_db(query,data):
            user = cls(connectToMySQL(User.db).query_db(query,data)[0])
            return user
        return False

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        if connectToMySQL(User.db).query_db(query,data):
            user = cls(connectToMySQL(User.db).query_db(query,data)[0])
            return user
        return False

    @staticmethod
    def validate_reg(form_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        valid = True

        if len(form_data['email']) < 1:
            flash("Email cannot be blank.","email")
            valid = False
        else:
            if not EMAIL_REGEX.match(form_data['email']):
                flash("Invalid email address.","email")
                valid = False
            else:
                if User.get_by_email(form_data):
                    flash("A user for that email already exists.","email")
                    valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long.","password")
            valid = False
        if not (form_data['password'] == form_data['confirm_password']):
            flash("Passwords must match.","password_confirm")
            valid = False
        if len(form_data['first_name']) < 3:
            flash("First name must be at least 3 characters long.","first_name")
            valid = False
        if len(form_data['last_name']) < 3:
            flash("Last name must be at least 3 characters long.","last_name")
            valid = False

        return valid

    @staticmethod
    def validate_login(form_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user = None

        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email/password.","login")
            return False

        user = User.get_by_email(form_data)
        if not user:
            flash("Invalid email/password.","login")
            return False
        
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Invalid email/password.","login")
            return False
        
        return user