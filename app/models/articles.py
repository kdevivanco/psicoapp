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

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


#PENDIENTE MODIFICAR


class Article:

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.file = data['file']
        self.publication_link = data['publication_link']
        self.user_id = data['user_id']

    #Protege la pagina de rutas ingresadas manualmente por el usuario
    @classmethod
    def route_protection(cls,id,user_id):
        pass

    @classmethod 
    def create(cls,form_data,user_id):
        #MODIFICAR EL CREATE

        query = '''
                INSERT INTO publications ( title , description,brand,link,file,img_url,user_id, created_at, publication_link ) 
                VALUES ( %(title)s , %(description)s,%(brand)s,  %(link)s, %(file)s, %(img_url)s, %(user_id)s, NOW() , NOW());
                '''

        data = {
                "title": form_data['title'],
                "description" : form_data['description'],
                "brand" : form_data['brand'],
                "link": form_data['link'],
                "file" : form_data['file'],
                "img_url" : form_data['img_url'],
                "user_id" : user_id
            }

        publication_id = connectToMySQL('psicoapp').query_db(query,data)  
        publication = publication.classify(publication_id) 
        publication.add_to_wishlist(wishlist_id,user_id,publication_id) #Agrega el publicationo al wishlist 

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
        publication.creator  = Therapist.get_one(publication.user_id)
        return publication

    #Devuelve todos los publicationos creados por el usuario
    @classmethod
    def get_all_from_user(cls,user_id): 
        
        query = '''
                SELECT id FROM publications
                WHERE user_id = %(user_id)s;
                '''

        data = {
            'user_id' : user_id
        }

        #results es una lista de todos los publicationos creados por el usuario
        results = connectToMySQL('psicoapp').query_db(query,data)
        user_publications = []
        if results == False:
            return user_publications #evita que la lista itere si esque esta vacia para evitar un error
        
        for publication_id in results:
            publication = publication.classify(publication_id['id']) #clasifica cada publicationo: cada id esta en un diccionario por eso se le pasa esa variable
            user_publications.append(publication) #lo agrega a la lista de publicationos 
        
        return user_publications
    
    #Devuelve todas las publicaciones menos las del terapeuta. 
    #COMENTARIO: ESTA FUNCION SOLO SE LLAMA SI EL TIPO DE CUENTA ES PSICOLOGO
    @classmethod
    def get_all_but_user(cls,user_id): 
        
        query = '''
                SELECT publications.id FROM publications
                WHERE publications.user_id != %(user_id)s
                order by publications.created_at desc;'''

        data = {
            'user_id' : user_id
        }

        results = connectToMySQL('psicoapp').query_db(query,data)
        other_publications = []

        if results == 0 or len(results) == 0 or results = False:
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
            'id' : id
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
            "id" = publication_id
        }

        return connectToMySQL('psicoapp').query_db(query,data)
    



