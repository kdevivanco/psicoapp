from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
import json
from app.models.users import User
from app.models.categories import Category

import pdb
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Therapist(User):
    def __init__(self,data):
        super().__init__(data)
        self.linkedin = data['linkedin']
        self.cdr = data['cdr']
        self.metodo = data['metodo']
        self.categories = []
        self.publications = []
        self.articles = []
        self.education =[]
        

    @classmethod
    def validate_form(self,form_data):
        #VALIDACION
        pass


    @classmethod
    def create(self,form_data):
        query = '''
                INSERT INTO users ( name , email , password , type, linkedin, cdr, age, gender,modalidad,metodo, created_at ) 
                VALUES ( %(name)s  , %(email)s , %(password)s , %(type)s, %(linkedin)s ,%(cdr)s,%(age)s, %(gender)s , %(modalidad)s, %(metodo)s, NOW());
                '''

        data = {
            'email':form_data['email'],
            'name' :form_data['full_name'],
            'password' :form_data['password'],
            'type' :int(form_data['account_type']),
            'linkedin' : form_data['linkedin'],
            'cdr': form_data['cdr'],
            'age' : int(form_data['age']),
            'gender' : form_data['gender'],
            'modalidad': form_data['modalidad'],
            'metodo' : form_data['metodo']
            }
        
        
        flash('Register  succesful!','success')

        return  connectToMySQL('psicoapp').query_db(query,data)


    @classmethod
    def classify(cls,id): 
        
        query = '''SELECT * FROM users 
                where users.id = %(id)s '''

        data = {
            "id": id
        }
        results = connectToMySQL('psicoapp').query_db(query,data)
        if results == False or len(results) ==0:
            print('no list matches id')
            return False
        
        result = results[0]
        therapist = cls(result)
        therapist.categories = cls.get_categories(id)

        #therapist.publications = Publication.get_all_from_user(id)
        #therapist.articles = Article.get_all_from_user(id)
        #therapist.requests  = Message.get_requests(id)
        #therapist.education = cls.get_education(id) #IMPLEMENTAR ESTE METODO EN ESTE MODELO
        #therapist.categories = User.get_categories(id) #IMPLEMENTAR METODO EN CLASE USER
    
        #for product in therapist.products:
        #    therapist.product_count +=1
        
        return therapist

    @classmethod
    def get_categories(cls,user_id):
        query = '''
                SELECT category_id from user_categories
                where user_id = %(user_id)s;
                '''

        data = {
            'user_id':user_id
        }

        results = connectToMySQL('psicoapp').query_db(query,data) 
        user_categories = []
        for category_id in results:
            user_categories.append(Category.classify(category_id['category_id']))

        return user_categories


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

    