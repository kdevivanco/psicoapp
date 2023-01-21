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

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Publication:

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.file = data['file']
        self.publication_link = data['publication_link']
        self.user_id = data['user_id']
        self.publisher = data['publisher']
        self.date = data['date']
        self.created_at = data['created_at']


    @classmethod 
    def create(cls,file_name,form_data,user_id):

        query = '''
                INSERT INTO publications (title , description, file, publication_link, user_id, publisher, date, created_at)
                VALUES ( %(title)s , %(description)s,%(file)s , %(publication_link)s, %(user_id)s , %(publisher)s,%(date)s , NOW());
                '''

        data = {
            'title' : form_data['title'],
            'description' : form_data['description'],
            'file' : file_name,
            'publication_link' : form_data['publication_link'],
            'user_id' : user_id,
            'publisher' : form_data['publisher'],
            'date' : form_data['date']
            }

        publication_id = connectToMySQL('psicoapp').query_db(query,data)  
        publication = cls.classify(publication_id) 

        return publication

    #Construye el objeto publication, este metodo es llamado por create_new
    @classmethod
    def classify(cls,id): #construye publication como objeto de clase publication
        
        query = '''SELECT * FROM publications 
                where id = %(id)s '''

        data = {
            "id": id
        }
        results = connectToMySQL('psicoapp').query_db(query,data)
        if results == False:
            
            return False
        result = results[0]

        publication = cls(result)
        publication.creator  = User.get_one(publication.user_id)
        publication.file_path = (f'/pdfs/{publication.file}')
        return publication

    #Devuelve todos los publicationos creados por el usuario
    @classmethod
    def get_all_from_user(cls,user_id): 
        
        query = '''
                SELECT id FROM publications
                WHERE user_id = %(user_id)s;
                '''

        data = {
            'user_id': int(user_id)
        }

        results = connectToMySQL('psicoapp').query_db(query,data)
        
        publications = []
        if len(results) == 0 or results == False:
            return publications
        
        for publication in results:
            publications.append(cls.classify(publication['id']))
        
        return publications
    
    #Devuelve todas las publicaciones menos las del terapeuta. 
    #COMENTARIO: ESTA FUNCION SOLO SE LLAMA SI EL TIPO DE CUENTA ES PSICOLOGO
    @classmethod
    def get_all_but_user(cls,user_id): 
        
        query = '''
                SELECT publications.id FROM publications
                WHERE publications.user_id != %(user_id)s
                order by publications.created_at desc;'''

        data = {
            'user_id' : int(user_id)
        }

        results = connectToMySQL('psicoapp').query_db(query,data)
        other_publications = []

        if results == 0 or len(results) == 0 or results == False:
            return other_publications #evita que la lista itere si esque esta vacia para evitar un error
        
        for publication_id in results:
            publication = cls.classify(publication_id['id'])
            other_publications.append(publication)
        
        return other_publications

    #FALTA MODIFICAR
    @classmethod
    def edit(cls,form_data,id):

        query = '''
                UPDATE publications
                SET title = %(title)s,
                link = %(link)s,
                brand = %(brand)s,
                img_url = %(img_url)s,
                description = %(description)s,
                file = %(file)s
                where id = %(id)s'''

        data = {
            'title' : form_data['title'],
            'link' : form_data['link'],
            'brand' : form_data['brand'],
            'img_url' : form_data['img_url'],
            'description' : form_data['description'],
            'file' : form_data['file'],
            'id' : int(id)
        }

        result = connectToMySQL('psicoapp').query_db(query,data)
        if not result:
            flash('something went wrong','danger')
            return False
        
        flash('publication edited','success')
        return True

    #Borra un publication
    # EN EL CONTROLLER SE DEBE PONER PROTECCION DE RUTA 
    @classmethod
    def delete(cls,publication_id):

        query = '''DELETE FROM publications 
                    where id = %(id)s'''

        data = {
            "id": publication_id
        }

        return connectToMySQL('psicoapp').query_db(query,data)
    



