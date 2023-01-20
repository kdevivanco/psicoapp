from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
import json
from app.models.users import User
from app.models.categories import Category
from app.models.educations import Education
from app.models.publications import Publication
from app.models.articles import Article
from app.models.messages import Message


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
        

    # METODO PARA EL UPLOAD DE LOS FILES - TRABAJO LINA
# Método para guardar las imágenes en esta carpeta local
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

        flash('¡La imagen quedó cargada!', 'success')
        return connectToMySQL('psicoapp').query_db(query,data)



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
            'therapist_id':int(therapist_id),
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

        #UPDATE


    @classmethod
    def classify(cls,id): 
        
        query = '''SELECT * FROM users 
                where users.id = %(id)s '''

        data = {
            "id": int(id)
        }
        results = connectToMySQL('psicoapp').query_db(query,data)
        if results == False or len(results) ==0:
            print('no list matches id')
            return False
        
        result = results[0]
        therapist = cls(result)
        therapist.categories = cls.get_categories(id)

        therapist.publications = Publication.get_all_from_user(id)
        therapist.articles = Article.get_all_from_user(id)
        therapist.requests  = Message.get_requests(id) #FALTA CREAR
        therapist.education = Education.get_education(id) 

        gender = {
            'female': 'Mujer',
            'male': 'Hombre',
            'non_binary': 'No binario',
            'genderfluid': 'Fluido de Genero',
            'trans_female': 'Mujer transgénero',
            'trans_male': 'Hombre Transgénero',
            'agender': 'Agender',
            'other':'No especificado'
        }

        modalidad = {
            'office': 'Consultorio - Presencial',
            'hybrid': 'Hibrido - Presencial/Virtual',
            'remote': 'Remoto - Virtual'
        }
        therapist.modalidad = modalidad[therapist.modalidad]
        therapist.gender = gender[therapist.gender]

        return therapist

    @classmethod
    def get_categories(cls,user_id):
        query = '''
                SELECT category_id from user_categories
                where user_id = %(user_id)s;
                '''

        data = {
            'user_id':int(user_id)
        }

        results = connectToMySQL('psicoapp').query_db(query,data) 
        user_categories = []
        for category_id in results:
            user_categories.append(Category.classify(category_id['category_id']))

        return user_categories


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
            'id' : int(user_id)
        }

        return connectToMySQL('psicoapp').query_db(query,data)


    @classmethod
    def editar(self,form_data):
        #EDITAR PERFIL DESPUES DE CREADO
        pass