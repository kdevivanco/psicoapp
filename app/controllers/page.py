from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.users import User
from app.models.categories import Category
from app.models.therapists import Therapist
from app.decorators import login_required
import json
import pdb

page = Blueprint('page', __name__, template_folder='templates')

@page.route('/dashboard') # 1. cambie la ruta base de /home a /
def home():
    categories = Category.get_all()
    if 'user' not in session or session['user'] == None:
        #return redirect('/')
        logged = False
        return render_template('dashboard.html',logged = logged, categories = categories)
    else: 
        logged = True
        user_id = session['user']['id']
        user = User.get_one(user_id)

    return render_template('dashboard.html',logged = logged, categories = categories, user = user)