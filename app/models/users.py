from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
import json
import pdb
import hashlib
import smtplib
from email.mime.text import MIMEText
 
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
        self.city = data['city']
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
    
    @staticmethod
    def generate_confirmation_hash(email):
        email = email.encode()
        hash_object = hashlib.sha256()
        hash_object.update(email)
        hex_dig = hash_object.hexdigest()
        conf_string = str(hex_dig)
        conf_hash = ''
        for letter in conf_string[:6]:
            if type(letter) == int:
                conf_hash+=str(letter)
            elif type(letter) == str:
                conf_hash+=letter.upper()
            else:
                pass
        return conf_hash

    @staticmethod
    def send_confirmation_email(email, confirmation_hash):
        msg = MIMEText("Your confirmation code is: " + confirmation_hash)
        msg['Subject'] = 'Email Confirmation'
        msg['From'] = 'psicoappcd@gmail.com'
        msg['To'] = email

        # Connect to the email server using SSL
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to the email server
        server.login("kdevivanco@gmail.com", "pbfdbistyushqlin")

        # Send the email
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        # Close the connection to the email server
        server.quit()


    @classmethod
    def create(self,form_data):

        password = bcrypt.generate_password_hash(form_data['password'])
        confirmation_hash = User.generate_confirmation_hash(form_data['email'])
    
        query = '''
                INSERT INTO users ( name , email , password , type, confirmation_hash, validated,created_at ) 
                VALUES ( %(name)s  , %(email)s , %(password)s , %(account_type)s, %(confirmation_hash)s, %(validated)s, NOW());
                '''

        data = {
            'email':form_data['email'],
            'name' :form_data['full_name'],
            'account_type': form_data['account_type'],
            'password': password,
            'confirmation_hash': confirmation_hash,
            'validated': 0 #El usuario no ha validado el perfil
            }
        
        
        return  connectToMySQL('psicoapp').query_db(query,data) #retorna el id del usuario

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

        if len(results) == 0 or results == False:
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
            'id' : int(user_id)
        }
        results = connectToMySQL('psicoapp').query_db(query,data)

        if len(results) == 0:
            return False 
        return (cls(results[0]))



    @classmethod
    def fill_info_patient(cls,form_data,user_id):
        query = '''
                UPDATE users 
                SET 
                age = %(age)s,
                gender = %(gender)s,
                modalidad = %(modalidad)s,
                description = %(description)s,
                city = %(city)s,
                validated = 2
                where id = %(user_id)s
                '''

        data = {
            'user_id':int(user_id),
            'age' :form_data['age'],
            'gender' :form_data['gender'],
            'modalidad': form_data['modalidad'],
            'city':form_data['city'],
            'description' : form_data['description']
        }
        
        
        flash('Register  succesful!','success')

        return  connectToMySQL('psicoapp').query_db(query,data)




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
                "user_id": int(user_id),
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


    @classmethod
    def update_validated(cls,user_id,status):
        query = '''
            UPDATE users
            SET validated = %(status)s
            WHERE id = %(id)s;
        '''

        data ={
            'id':int(user_id),
            'status': status
        }

        connectToMySQL('psicoapp').query_db(query,data)
        return

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
            'id':int(user_id),
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'profile_url': form_data['profile_url']
        }

        connectToMySQL('psicoapp').query_db(query,data)
        return




