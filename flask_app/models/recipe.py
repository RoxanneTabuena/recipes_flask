from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def create(cls, data):
        query = """INSERT INTO recipes
        (name, under_30, description, instructions, date_made, user_id) VALUES
        ( %(name)s, %(under_30)s, %(description)s, %(instructions)s,
        %(date_made)s, %(user_id)s)"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id"
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for row in results:
            recipe = (cls(row))
            author = {
                        'id': row['users.id'],
                        'first_name':row['first_name'],
                        'last_name':row['last_name'],
                        'email':row['email'],
                        'password':row['password'],
                        'created_at':row['created_at'],
                        'updated_at':row['updated_at']
            }
            creator = User(author)
            recipe.creator = creator
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_one(cls, id):
        data = {'id' : id}
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)[0]
        recipe = cls(result)
        author = {
            'id': result['users.id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'password': result['password'],
            'created_at': result['created_at'],
            'updated_at': result['updated_at']
            }
        creator = User(author)
        recipe.creator = creator
        return recipe

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, under_30 = %(under_30)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Enter a valid name!")
            is_valid = False
        elif len(data['instructions']) <3:
            flash("Enter valid instructions!")
            is_valid = False
        elif len(data['description']) < 3:
            flash("Enter a valid description!")
            is_valid = False
        return is_valid
