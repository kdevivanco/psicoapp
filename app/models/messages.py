from app import app
from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import json
import pdb
from app.models.users import User

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.reciever_id = data['reciever_id']
        self.text = data['text']
        self.created_at = data['created_at']
        self.status = data['status']

#CAMBIAR QUERIES
#Crea un request de un usuario no creador para unirse al wishlist
    @classmethod
    def send_msg(cls,sender_id,reciever_id,form_data):
        query = '''
                INSERT INTO mensajes ( sender_id , reciever_id, text, created_at,status ) 
                VALUES ( %(sender_id)s , %(reciever_id)s, %(text)s, NOW() ,"sent");
                '''

        data = {
                "sender_id": sender_id,
                "reciever_id" : reciever_id,
                'text' : form_data['text']
            }
        
        message_id = connectToMySQL('psicoapp').query_db(query,data) 

        if message_id == None or message_id == False: 
            flash('Something went wrong')
            return False
        else:
            return message_id

    @classmethod
    def respond_msg(cls,id):
        query = '''
                UPDATE mensajes
                SET status = "read"
                WHERE id = %(id)s
                '''

        data = {
                'id':id
            }
        
        return connectToMySQL('psicoapp').query_db(query,data) 

    @classmethod
    def get_all_messages(cls,reciever_id): #FALTA MODIFICAR!!!
        query = '''SELECT * FROM mensajes 
                where reciever_id = %(reciever_id)s '''

        data = {
            "reciever_id": int(reciever_id)
        }
        
        results = connectToMySQL('psicoapp').query_db(query,data) 

        messages =[] 

        if results == False or len(results) == 0:
            return messages

        for result in results:
            message = (cls(result))
            message.sender = User.get_one(message.sender_id)
            messages.append(message)

        return messages
