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
    def fill_info(self,form_data,therapist_id):
        query = '''
                UPDATE users 
                SET 
                linkedin = %(linkedin)s,
                cdr = %(cdr)s,
                age = %(age)s,
                gender = %(gender)s,
                modalidad = %(modalidad)s,
                description = %(description)s,
                metodo = %(metodo)s,
                validated = 2
                where id = %(therapist_id)s
                '''

        data = {
            'therapist_id':therapist_id,
            'linkedin' : form_data['linkedin'],
            'cdr':form_data['cdr'],
            'age' :form_data['age'],
            'gender' :form_data['gender'],
            'modalidad': form_data['modalidad'],
            'description' : form_data['description'],
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
    def add_education(cls,form_data,user_id):

        query = '''
                INSERT INTO education ( school_name,  title_name, description, therapist_id)
                VALUES ( %(school_name)s, %(title_name)s, %(description)s, %(therapist_id)s);
                '''

        data = {
            'school_name' :form_data['school_name'],
            'title_name': form_data['title_name'],
            'description': form_data['description'],
            'therapist_id': user_id
            }
        
        
        return  connectToMySQL('psicoapp').query_db(query,data)

    @classmethod
    def get_education(cls,therapist_id):
        query = '''
                SELECT * from education where therapist_id = %(therapist_id)s;
                '''

        data = {
            'therapist_id': therapist_id
        }

        results = connectToMySQL('psicoapp').query_db(query,data)
        pdb.set_trace()
        education_list = []
        for education in results:
            education_list.append(education)
        
        return education_list


    #Valida al usuario segun el estatus en el que esta
    @classmethod
    def update_validated(cls,step,user_id):
        if step == 'email':
            valid = 1
        elif step == 'info':
            valid = 2
        elif step == 'education':
            valid = 3
        else: 
            return False
        
        query = '''
                UPDATE users
                SET validated = %(valid)s
                where id = %(id)s'''

        data = {
            'valid' : valid,
            'id' : user_id
        }

        return connectToMySQL('psicoapp').query_db(query,data)


    @classmethod
    def editar(self,form_data):
        #EDITAR PERFIL DESPUES DE CREADO
        pass


# METODO PARA EL UPLOAD DE LOS FILES
# Agrega el path de las imagenes de acá en la base de datos 
    @classmethod
    def set_profile_pic(self, email, filename):
        query = '''
                UPDATE users 
                SET profile_pic = %(profile_pic)s
                WHERE email = %(email)s
                '''

        data = {
            'email': email,
            'profile_pic': filename
        }

        flash('imagen subida con éxito', 'success')
        return connectToMySQL('psicoapp').query_db(query,data)