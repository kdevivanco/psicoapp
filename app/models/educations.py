from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
import json
import pdb



class Education:

    def __init__(self,data):
        self.id = data['id']
        self.school_name = data['school_name']
        self.title_name = data['title_name']
        self.description = data['description']
        self.therapist_id = data['therapist_id']

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
        education_list = []
        for education in results:
            education_list.append(cls(education))
        
        return education_list