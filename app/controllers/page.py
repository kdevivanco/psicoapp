from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.users import User
from app.models.categories import Category
from app.models.therapists import Therapist
from app.decorators import login_required
from app.models.articles import Article
from app.models.locations import Location
import json
import pdb

page = Blueprint('page', __name__, template_folder='templates')

@page.route('/dashboard') # 1. cambie la ruta base de /home a /
def home():
    categories = Category.get_all()
    if 'user' not in session or session['user'] == None:
        logged = False
        return render_template('dashboard.html',logged = logged, categories = categories)

    logged = True
    user_id = session['user']['id']
    user = User.get_one(user_id)
    all_articles = Therapist.get_other_articles(user_id)
    locations = Location.city_districts(user.city)

    return render_template('dashboard.html',logged = logged, categories = categories, user = user, all_articles = all_articles,locations=locations)


# @page.route('/search-therapist', methods=['POST'])
# def search_a_therapist():
#     pdb.set_trace()

#     return render_template('found_therapists.html')

@page.route('/change-city')
@login_required
def show_change_city():
    all_cities = Location.get_all()

    return render_template('change_city.html', all_cities = all_cities)

@page.route('/change-city', methods=['POST'])
@login_required
def change_city():
    pdb.set_trace()
    Location.change(request.form,session['user']['id'])

    return redirect('/dashboard')

#SEARCHES


@page.route('/search-therapist',methods=['POST'])
def search_therapist():
    text = request.form['text']
    path = (f'/search/{text}')

    return redirect(path)

@page.route('/search/<text>')
def show_results(text):
    results = Therapist.search(text)
    return render_template('search_results.html',text = text,results=results)

#SEARCH CITY
@page.route('/search-city')
def search_city():
    pdb.set_trace()
    Location.change(request.form,session['user']['id'])

    return redirect('/dashboard')

@page.route('/search-district',methods=['POST'])
@login_required
def search_district():
    if 'user' not in session or session['user']==None:
        flash('Debes registrate para acceder a esta función', 'primary')
        return redirect('/register')
    logged = True
    
    user = User.get_one(session['user']['id'])
    
    location_id = request.form['location_id']

    results = Therapist.search_location(location_id)

    location = Location.get_one(location_id)
    pdb.set_trace()

    text = (f'{location.city}, {location.district}')

    return render_template('search_results.html',results=results,text=text,user=user, location = location, logged = logged)

@page.route('/search-cat', methods=['POST'])
def search_category():
    if 'user' not in session or session['user']==None:
        logged = False
    else:
        logged = True
        category_id = request.form['category_id']
        results = Therapist.search_cat(category_id)
        category = Category.classify(category_id)
        text = category.name
        user = User.get_one(session['user']['id'])

    return render_template('search_results.html',results=results,text=text,user=user, logged = logged)
    



