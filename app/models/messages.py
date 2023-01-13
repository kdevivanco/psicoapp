from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
from app import app
import json
from app.models.patients import Patient
from app.models.therapits import Therapist
import pdb
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


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
                INSERT INTO participants ( participant_id , wishlist_id, status ) 
                VALUES ( %(participant_id)s , %(wishlist_id)s, "requested");
                '''

        data = {
                "participant_id": participant_id,
                "wishlist_id" : wishlist_id
            }
        return connectToMySQL('wishlist2').query_db(query,data) 

    @classmethod
    def respond_msg(cls,sender_id,reciever_id,status):
        query = '''
                UPDATE participants
                SET status = %(status)s
                WHERE participant_id = %(participant_id)s and wishlist_id = %(wishlist_id)s;
                '''

        data = {
                "status": status,
                "participant_id": participant_id,
                "wishlist_id" : wishlist_id
            }
        
        return connectToMySQL('wishlist2').query_db(query,data) 
