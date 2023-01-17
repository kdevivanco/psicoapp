from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
import json
import pdb
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.age = data['age']
        self.gender = data['gender']
        self.description = data['description']
        self.type = data['type']
        self.created_at = data['created_at']
        self.modalidad = data['modalidad']
        self.confirmation_hash = data['confirmation_hash']
        self.validated = data['validated']
        self.messages = []
        #self.linkedin = data['linkedin']
        #self.profile_pic = data['profile_pic']
        #self.cdr = data['cdr']


    #Crea una lista de todos los usuarios y los devuelve como objetos User   
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL('psicoapp').query_db('select * from users')
        users = []
        for user in results:
            users.append(cls(user))
        
        return users

    #Validacion del registro
    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if len(form_data['full_name']) <4:
            flash("Name must be at least 4 characters.",'error')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!",'error')
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters.",'error')
            is_valid = False
        if form_data["password"] != form_data["confirm_password"]:
            flash('Passwords must match!','error')
            is_valid = False
        if is_valid == True:
            flash('Valid credentials! Please fill in aditional info', 'info')
        return is_valid

    #Verifica que el correo de registro este o no en la base de datos
    @classmethod
    def email_free(cls,form_data):
        query = '''
                SELECT * FROM users where email = %(email)s
        '''
        data = {
            'email' : form_data['email']
        }

        results = connectToMySQL('psicoapp').query_db(query, data)
        
        if len(results) == 0:
            return True
        else:
            flash("Email already in database",'error')
            print( 'Email not available')
            return False
    

    @classmethod
    def encrypt_pass(cls,pswd):
        password = bcrypt.generate_password_hash(pswd)
        return password


    #Crea un nuevo usuario y encrypta su contrasena, esa contrasena encriptada es guardada a la base de datos
    @classmethod
    def create(cls,form_data):

        query = '''
                INSERT INTO users ( name , email , password , type, created_at ) 
                VALUES ( %(name)s  , %(email)s , %(password)s , %(type)s, NOW());
                '''

        data = {
                "name": form_data["name"],
                "email" : form_data["email"],
                "type" : form_data["type"],
                "password" : password
            }
        
        
        flash('Register  succesful!','success')

        return  connectToMySQL('psicoapp').query_db(query,data)

    #Verifica el login de dos formas:
    #1. que el usuario exista en la base de datos 
    #2.Que las contrasenas sean iguales
    @classmethod
    def login(cls,form_data):
        print(form_data['email'])
        query = '''
                SELECT * FROM users where email = %(email)s;
                '''
        
        data = {
            "email":form_data['email']
        }

        results= connectToMySQL('psicoapp').query_db(query,data)

        if len(results) == 0:
            flash('User not registered','error')
            print('User not in database')
            return False

        user =cls(results[0])
        print(user)
        result = bcrypt.check_password_hash(user.password,form_data['password'])

        if result == True:
            return user
        else:
            flash('Invalid credentials','error')
            return False

    #Retorna un usuario como clase User
    @classmethod
    def get_one(cls,user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        data = {
            'id' : user_id
        }
        results = connectToMySQL('psicoapp').query_db(query,data)

        if len(results) == 0:
            return False 
        return (cls(results[0]))

    @classmethod
    def add_address(cls,user_id,location_id):
        query = '''
                INSERT INTO address ( user_id , location_id) 
                VALUES ( %(user_id)s , %(location_id)s);
                '''

        data = {
                "user_id": user_id,
                "location_id" : location_id
            }
        return connectToMySQL('psicoapp').query_db(query,data) 
        pass


    @classmethod
    def update_address(cls,user_id,location_id):
        query = '''
                UPDATE address 
                SET location_id = %(location_id)s
                WHERE user_id = %(user_id)s;
                '''

        data = {
                "user_id": user_id,
                "location_id" : location_id
            }
        return connectToMySQL('psicoapp').query_db(query,data) 
        pass


    @classmethod
    def add_category(cls,user_id,category_id):
        query = '''
                INSERT INTO category ( user_id , category_id) 
                VALUES ( %(user_id)s , %(category_id)s);
                '''

        data = {
                "user_id": user_id,
                "category_id" : category_id
            }
        return connectToMySQL('psicoapp').query_db(query,data) 
        pass




    #UPDATE FOR USER
    @classmethod
    def edit(cls,user_id,form_data):
        query = '''
            UPDATE users
            SET first_name = %(first_name)s,
            last_name = %(last_name)s,
            profile_url = %(profile_url)s
            WHERE id = %(id)s;
        '''

        data ={
            'id':user_id,
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'profile_url': form_data['profile_url']
        }

        connectToMySQL('psicoapp').query_db(query,data)
        return




