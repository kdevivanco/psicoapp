# from app.config.connections import MySQLConnection, connectToMySQL
# from flask import flash
# import re	
# from app import app
# from flask_bcrypt import Bcrypt        
# import json
# import pdb
# bcrypt = Bcrypt(app)


# @classmethod
#     def create(cls,form_data):

#         query = '''
#                 INSERT INTO users ( name , email , password , type, created_at ) 
#                 VALUES ( %(name)s  , %(email)s , %(password)s , %(type)s, NOW());
#                 '''

#         data = {
#                 "name": form_data["name"],
#                 "email" : form_data["email"],
#                 "type" : form_data["type"],
#                 "password" : password
#             }
        
        
#         flash('Register  succesful!','success')

#         return  connectToMySQL('psicoapp').query_db(query,data)