from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def retrieve_via_email(cls, data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def retrieve_via_id(cls, id):
        data = {'id' : id}
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name']) < 3 or data['first_name'].isalpha() == False:
            flash("Enter a valid first name!")
            is_valid = False
        elif len(data['last_name']) < 3 or data['last_name'].isalpha() == False:
            flash("Enter a valid last name!")
            is_valid = False
        elif len(data['email']) == 0 or not EMAIL_REGREX.match(data['email']):
            flash("Enter a valid email!")
            is_valid = False
        elif User.retrieve_via_email(data) != False:
            flash("We already have a user under that email")
            is_valid = False
        elif len(data['password']) < 8:
            flash('Enter a longer password')
            is_valid = False
        elif data['unhashed_pw'] != data['password_conf']:
            flash("Dem passwords dont match")
            is_valid = False
        return is_valid
