from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.users import User
from app.models.categories import Category
from app.models.therapists import Therapist
from app.decorators import login_required
import json
import pdb

users = Blueprint('users', __name__, template_folder='templates')

def mydecorator(): #esta funcion actua como un decorador solo para usarla en el landing page:
    if 'user' not in session or session['user'] == None : #si no hay sesion:
        return False
    log = 'logout'
    user = session['user']
    return (log,user)


@users.route('/')
def landing_page():
    if 'user' not in session or session['user'] == None:
        log = 'Log in'
    else:
        log = 'Log out'

    therapist = Therapist.classify(session['user']['id']) #FUNCIONA PARA TERAPEUTA Y LISTA DE CATEGORIAS, FALTA EDUCACION! 

    return render_template('landing.html', log = log)

@users.route('/register')
def show_register():
    return render_template('register.html')


@users.route('/register',methods=["POST"])
def register_user():
    if not User.email_free(request.form):
        return redirect('/register')
    if not User.validate_user(request.form):
        return redirect('/register')
    
    password = User.encrypt_pass(request.form['password'])

    session['user'] = {
        'id': None,
        'email' : request.form['email'],
        'full_name' : request.form['full_name'],
        'password' : password,
        'account_type' : request.form['account_type']
    }

    #pdb.set_trace()
    if int(request.form['account_type']) == 0: 
        #the user type is a therapist
        return redirect('/therapist-reg')
    else: 
        return redirect('/patient-reg')

@users.route('/therapist-reg')
def show_therapist_register():
    
    all_categories = Category.get_all()
    
    #pdb.set_trace()
    #if ['user'] not in session or session['user'] == None:
    #    return redirect('/')

    return render_template('register_therapist.html', all_categories = all_categories)


@users.route('/therapist-reg', methods = ['POST'])
def register_therapist():
    if 'user' not in session or session['user'] == None:
        return redirect('/')
    user_data = {
        'email': session['user']['email'],
        'full_name' : session['user']['full_name'],
        'password' : session['user']['password'],
        'account_type' : session['user']['account_type'],
        'linkedin' : request.form['linkedin'],
        'cdr': request.form['cdr'],
        'age' : request.form['age'],
        'gender' : request.form['gender'],
        'modalidad': request.form['modalidad'],
        'metodo' : request.form['metodo']
    }
    selected_categories = request.form.getlist('category')

    session['user']['id'] = Therapist.create(user_data)
    for cat_id in selected_categories:
        Category.add_to_category(session['user']['id'],int(cat_id))

    return redirect('/')#/add-education.html'

@users.route('/login')
def show_login():
    #if 'user' in session:
    #    return redirect('/log')
    return render_template('login.html')

@users.route('/login',methods=["POST"])
def login():
    user = User.login(request.form)
    if user != False:
        session['user'] = {
            'id': user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'profile_url':user.profile_url
        }
    else:
        return redirect('/login')

    return redirect('/dashboard')


@users.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')


@users.route('/edit-profile/<id>')
@login_required
def show_edit_profile(id):
    log,user = mydecorator()
    user_id = user['id']
    if user['id'] != int(id):
        return redirect('/dashboard')

    this_user = User.get_one(user['id'])

    return render_template('edit_profile.html', user=user, this_user = this_user)


@users.route('/edit-profile/<id>',methods=['POST'])
@login_required
def edit_profile(id):
    log,user = mydecorator()
    user_id = user['id']
    if user['id'] != int(id):
        return redirect('/dashboard')
    edited_user = User.get_one(user_id)
    User.edit(user['id'],request.form)
    session['user'] = {
            'id': edited_user.id,
            'first_name':edited_user.first_name,
            'last_name':edited_user.last_name,
            'email':edited_user.email,
            'profile_url':edited_user.profile_url
        }
    
    return redirect('/dashboard')

@users.route('/profile/<id>')
@login_required
def show_profile(id):
    if 'user' not in session or session['user'] == None : #si no hay sesion:
        return False
    log,user = mydecorator()
    user_id = user['id']
    creator = Wishlist.get_all_from_user(id)
    this_user = User.get_one(id)
    
    user_products = Product.get_all_from_user(id)

    return render_template('view_profile.html',user=user,creator=creator, user_products = user_products,this_user = this_user, log = log)