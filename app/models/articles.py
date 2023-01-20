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


#PENDIENTE MODIFICAR


class Article:

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.subtitle = data['subtitle']
        self.body = data['body']
        self.created_at = data['created_at']
        self.img_filename = data['img_filename']
        self.bibliography = data['bibliography']
        self.user_id = data['user_id']
        self.file_path = ''

    #Protege la pagina de rutas ingresadas manualmente por el usuario
    @classmethod
    def route_protection(cls,id,user_id):
        pass

    @classmethod 
    def create(cls,file_name,form_data,user_id):
        #MODIFICAR EL CREATE

        query = '''
                INSERT INTO articles (title, subtitle, body, img_filename, user_id, created_at) 
                VALUES ( %(title)s, %(subtitle)s,%(body)s, %(img_filename)s, %(user_id)s, NOW());
                '''

        data = {
                "title": form_data['title'],
                "subtitle": form_data['subtitle'],
                "body" : form_data['body'],
                "img_filename" : file_name,
                "bibliography": form_data['bibliography'],
                "user_id" : user_id
            }

        article_id = connectToMySQL('psicoapp').query_db(query,data)  
        article = cls.classify(article_id) 

        return article

    #Construye el objeto publication, este metodo es llamado por create_new
    @classmethod
    def classify(cls,id): #construye publication como objeto de clase publication
        
        query = '''SELECT * FROM articles 
                where id = %(id)s '''

        data = {
            "id": int(id)
        }
        results = connectToMySQL('psicoapp').query_db(query,data)
        if results == False:
            
            return False
        result = results[0]

        article = cls(result)
        article.creator  = User.get_one(article.user_id)
        article.file_path = (f'img/articles/{article.img_filename}')
        article.body = article.body.replace('\n', '<br>')

        return article

    #Devuelve todos los articulos creados por el usuario
    @classmethod
    def get_all_from_user(cls,user_id): 
        
        query = '''
                SELECT id FROM articles
                WHERE user_id = %(user_id)s;
                '''

        data = {
            'user_id' : user_id
        }
        results = connectToMySQL('psicoapp').query_db(query,data)
        
        articles = []
        if len(results) == 0 or results == False:
            return articles

        for article in results:
            articles.append(cls.classify(article['id']))
        
        return articles
        
    
    #Devuelve todas las publicaciones menos las del terapeuta. 
    #COMENTARIO: ESTA FUNCION SOLO SE LLAMA SI EL TIPO DE CUENTA ES PSICOLOGO
    @classmethod
    def get_all_but_user(cls,user_id): 
        
        query = '''
                SELECT articles.id FROM articles
                WHERE articles.user_id != %(user_id)s
                order by articles.created_at desc;'''

        data = {
            'user_id' : user_id
        }

        results = connectToMySQL('psicoapp').query_db(query,data)
        other_articles = []

        if results == 0 or len(results) == 0 or results == False:
            return other_articles #evita que la lista itere si esque esta vacia para evitar un error
        

        for article_id in results:
            article = cls.classify(article_id['id'])
            other_articles.append(article)
        
        return other_articles

    #FALTA MODIFICAR
    @classmethod
    def edit(cls,form_data,id):

        query = '''
                UPDATE articles
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

        query = '''DELETE FROM articles 
                    where id = %(id)s'''

        data = {
            "id": int(publication_id)
        }

        return connectToMySQL('psicoapp').query_db(query,data)
    



