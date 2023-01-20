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