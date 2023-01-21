from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
from flask_bcrypt import Bcrypt        
import json
import pdb



class Location:

    def __init__(self,data):
        self.id = data['id']
        self.city = data['city']
        self.district = data['district']

    @classmethod
    def get_all(cls):

        query = '''
                SELECT city from location;
                '''

        cities = connectToMySQL('psicoapp').query_db(query)

        all_cities = []

        for city in cities:
            all_cities.append(city['city'])
        
        all_cities = set(all_cities)
        all_cites = list(all_cities)
        
        return  all_cities

    
    @classmethod
    def city_districts(cls,city_name):

        query = '''
            SELECT * from location where city = %(city_name)s;
            '''

        data = {
        'city_name': (city_name)
        }

        results = connectToMySQL('psicoapp').query_db(query,data)
        locations = []
        for location in results:
            locations.append(cls(location))
        
        return locations

    @classmethod
    def change(cls,form_data,user_id):
        query = '''
            UPDATE users
            SET city = %(city_name)s
            WHERE id = %(id)s;
            '''

        data = {
        'city_name': form_data['city'],
        'id': user_id
        }

        connectToMySQL('psicoapp').query_db(query,data)
        
        return 

    @classmethod
    def log_location(cls,location_id,user_id):
        query = '''
                INSERT INTO address ( location_id , user_id) 
                VALUES ( %(location_id)s , %(user_id)s);
                '''

        data = {
                "location_id": location_id,
                "user_id" : user_id
            }
        
        connectToMySQL('psicoapp').query_db(query,data) 
        
        return

    @classmethod
    def get_address(cls,user_id):
        query = '''
                SELECT * from location
                WHERE id =
                (SELECT location_id from address
                WHERE user_id = %(user_id)s);
                '''

        data = {
                "user_id" : user_id
            }
        
        results = connectToMySQL('psicoapp').query_db(query,data) 
        if results == False or len(results) == 0 or results == []:
            return ''
        
        location = cls(results[0])
    
        return location

    @classmethod
    def get_one(cls,id):
        query = '''
                SELECT * from location
                WHERE id = %(id)s;
                '''

        data = {
                "id" : id
            }
        
        results = connectToMySQL('psicoapp').query_db(query,data) 
        if results == False or len(results) == 0 or results == []:
            return ''
        
        location = cls(results[0])
    
        return location
    
