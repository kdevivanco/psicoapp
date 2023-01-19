from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.users import User
from app.models.categories import Category
from app.models.therapists import Therapist
from app.decorators import login_required
import json
import pdb

users = Blueprint('users', __name__, template_folder='templates')

def pseudodecorador():
    if 'user' not in session or session['user'] == None:
        return False
    else:
        return True

# RUTAS DE INICIO
@users.route('/') # 1. cambie la ruta base de /home a /
def home():
    logged = pseudodecorador()
    if not logged:
        return render_template('index.html',logged=logged)
    else: 
        user_id = int(session['user']['id'])
        return redirect(f'/dashboard') # 2. en esta ruta hay que agregar logica para redireccionar dependiendo del tipo de usuario



def mydecorator(): #esta funcion actua como un decorador solo para usarla en el landing page:
    if 'user' not in session or session['user'] == None : #si no hay sesion:
        return False
    log = 'logout'
    user = session['user']
    return (log,user)


# REGISTRO INICIAL DE CUALQUIER USUARIO
@users.route('/register')
def show_register():
    return render_template('register_psicoapp.html')

@users.route('/register',methods=["POST"])
def register_user():
    if not User.email_free(request.form):
        return redirect('/register')
    if not User.validate_user(request.form):
        return redirect('/register')

    user_id = int(User.create(request.form))#INSERTA AL USUARIO SIN IMPORTAR DE QUE TIPO ES    
    user = User.get_one(user_id)
    if user != False:
        session['user'] = {
            'id': int(user.id),
            'name':user.name,
            'email':user.email,
            'type':user.type
        }

    if int(request.form['account_type']) == 0: 
        #the user type is a therapist
        return redirect('/therapist-reg')
    else: 
        return redirect('/patient-reg')



# # TERMINAR EL REGISTRO DEL USUARIO
# @users.route('/user-reg')
# def edit_user():
#     return render_template('reg_user.html')


# LOGIN DE CUALQUIER USUARIO
#falta anadir logica para si el usia
@users.route('/login')
def show_login():
    return render_template('log_in.html')

@users.route('/login',methods=["POST"])
def login():
    user = User.login(request.form)
    if user != False:
        session['user'] = {
            'id': int(user.id),
            'name':user.name,
            'email':user.email,
            'type':user.type
        }
    else:
        return redirect('/falta-validar')

        return redirect('/login')
    if user.validated == 0:
        #Falta verificar email 
        #Mandar a verifica tu email
        pass
    if user.type == 0 and user.validated == 1: #Ha verificado su email pero no llenado info de psicologo
        #redirecionamos a terminar perfil
        return redirect('/therapist-reg')
    elif user.type == 0 and user.validated == 2:
        return redirect('/add-education')
    elif user.type == 0 and user.validated == 3: 
        return redirect(f'/tprofile/{user.id}')
    return redirect('/dashboard') # No estoy muy segura a dónde debe llevar al usuario, estaba /dashboard, pero creo que este punto entra al perfil del usuario o del terapeuta

# ENTRA AL PERFIL DEL USUARIO

@users.route('/profile_user')
def profile_user():
    return render_template('profile_user.html')


# LOG OUT DE CUALQUIER USUARIO
@users.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')





# EDITAR LOS USUARIOS
@users.route('/edit_user/<id>')
@login_required
def show_edit_profile(id):
    log,user = mydecorator()
    user_id = int(user['id'])
    if user['id'] != int(id):
        return redirect('/profile_user')

    this_user = User.get_one(user['id'])

    return render_template('edit_user.html', user=user, this_user = this_user)


@users.route('/edit_user/<id>',methods=['POST'])
@login_required
def edit_profile(id):
    log,user = mydecorator()

    user_id = int(user['id'])

    if user['id'] != int(id):
        return redirect('/profile_user')

    edited_user = User.get_one(user_id)
    User.edit(user['id'],request.form)

    session['user'] = {
            'id': edited_user.id,
            'first_name':edited_user.first_name,
            'last_name':edited_user.last_name,
            'email':edited_user.email,
            'profile_url':edited_user.profile_url
        }
    
    return redirect('/profile_user')
