
from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
from app.models.users import User
#from app.models.lists import Wishlist
import pdb
import time
bcrypt = Bcrypt(app)



# Metodos: cognitivo-conductual, psicoanálisis, humanismo y sistémica.
# Categorias: addiciones, depresion, ansiedad, adolescentes, familiar, 
class Category:

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']


    #CLASS METHOD PARA FILTRR POR CATEGORIA
    #CASO BASE - SOLO UNA CATEOGRIA


    @classmethod
    def classify(cls,category_id):
        query = '''
                SELECT * from categories
                where id = %(id)s;
                '''

        data = {
            'id': int(category_id)
        }

        results = connectToMySQL('psicoapp').query_db(query,data) 
        category = cls(results[0])

        return category


    @classmethod
    def get_all(cls):
        query = '''
                SELECT * from categories;
                '''

        return connectToMySQL('psicoapp').query_db(query) 


    @classmethod
    def add_to_category(cls,user_id,category_id):
        query = '''
                INSERT INTO user_categories ( user_id , category_id ) 
                VALUES ( %(user_id)s , %(category_id)s);
                '''

        data = {
                "user_id": user_id,
                "category_id" : category_id
            }
        return connectToMySQL('psicoapp').query_db(query,data) 


