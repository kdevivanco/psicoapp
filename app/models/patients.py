from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
import json
from app.models.users import User
import pdb
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



#ACTUALIZAR SEGUN PARAMTEROS DE PACIENTES


class Patient(User):
    def __init__(self,data):
        super().__init__(data)

    @classmethod
    def validate_form(self,form_data):
        #VALIDACION
        pass

    @classmethod
    def anadir_datos(self,form_data):
        #1.  toma el form especifico para usuarios y agrega los nuevos datos a la base de datos: AGREGA GENDER, AGE, MODALIDAD 

        #2. AGREGA LA DIRECCION: LLAMA A FUNCION ADD_ADDRESS

        #3. AGREGA CATEGORIAS

        pass

    @classmethod
    def classify(cls,id): 
        
        query = '''SELECT * FROM users 
                where users.id = %(id)s '''

        data = {
            "id": id
        }

        results = connectToMySQL('wishlist2').query_db(query,data)
        if results == False or len(results) ==0:
            print('no list matches id')
            return False
        
        result = results[0]
        patient = cls(result)

        patient.requests  = Message.get_requests(id)
        patient.categories = User.get_categories(id) #IMPLEMENTAR METODO EN CLASE USER
    
        for product in patient.products:
            patient.product_count +=1
        
        return patient

    
    @classmethod
    def editar(self,form_data):
        #EDITAR PERFIL DESPUES DE CREADO
        pass

    