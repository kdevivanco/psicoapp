
from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
from app.models.users import User
from app.models.therapists import Therapist
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


    #CASO COMUN - 2 + CATEGORIAS (como maximo 4)