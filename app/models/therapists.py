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


class Therapist(User):
    def __init__(self,data):
        super().__init__(data)
        self.linkedin = data['linkedin']
        self.profile_pic = data['profile_pic']
        self.cdr = data['cdr']
        self.metodo = data['metodo']
        self.publications = []
        self.articles = []
        self.education =[]
        

    @classmethod
    def validate_form(self,form_data):
        #VALIDACION
        pass


    @classmethod
    def anadir_datos(self,form_data):
        # toma el form especifico para psicologos y agrega los nuevos datos a la base de datos
        #1. INSERT A LA TABLA USERS CON LA INFO ADICIONAL: LINKEDIN, FOTO, CDR 

        #2. AGREGA LA DIRECCION: LLAMA A FUNCION ADD_ADDRESS

        #3. LLAMA A LA FUNCION ADD_EDUCATION  // FOR LOOP PARA CADA EDUCACION

        #4. AGREGA CATEGORIAS // FOR LOOP QUE AGREGA A LA FUNCION ADD_CATEOGRIES

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
        therapist = cls(result)

        therapist.publications = Publication.get_all_from_user(id)
        therapist.articles = Article.get_all_from_user(id)
        therapist.requests  = Message.get_requests(id)
        therapist.education = cls.get_education(id) #IMPLEMENTAR ESTE METODO EN ESTE MODELO
        therapist.categories = User.get_categories(id) #IMPLEMENTAR METODO EN CLASE USER
    
        for product in therapist.products:
            therapist.product_count +=1
        
        return therapist

        
    @classmethod
    def add_education(cls,user_id,form_data):
        pass 
        # school_name
        # title_name
        # description
        # therapist_id

    @classmethod
    def get_education(id):
        #QUERY LLAMA A LA TABLA EDUCATION DONDE EL ID == USER_ID 
        pass


    @classmethod
    def editar(self,form_data):
        #EDITAR PERFIL DESPUES DE CREADO
        pass

    