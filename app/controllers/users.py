from flask import Flask, render_template, request, redirect, Blueprint,session,flash
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
    user= User.get_one(session['user']['id'])
    User.send_confirmation_email(user.email, user.confirmation_hash)
    return redirect('/validate-email')
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
    if user == False:
        return redirect('/login')

    session['user'] = {
        'id': int(user.id),
        'name':user.name,
        'email':user.email,
        'type':user.type
    }

    if user.validated == 0:
        return redirect('/validate-email')
        pass
    elif user.type == 1 and user.validated < 2:
        return redirect('/patient-reg')
    elif user.type == 0 and user.validated == 1: #Ha verificado su email pero no llenado info de psicologo
        return redirect('/therapist-reg')
    elif user.type == 0 and user.validated == 2: #Ha llenado informacion de psicologo
        return redirect('/add-education')
    elif user.type == 0 and user.validated == 3:  #ha llenado informacion de educacion
        return redirect(f'/tprofile/{user.id}')
    return redirect('/dashboard') #


@users.route('/validate-email')
@login_required
def show_validate():
    user= User.get_one(session['user']['id'])
    logged = True 
    return render_template('finish_valid.html',logged= logged, user = user)

@users.route('/send-validation')
@login_required
def send_validate():
    user= User.get_one(session['user']['id'])
    User.send_confirmation_email(user.email, user.confirmation_hash)
    flash('Código enviado', 'info')
    return redirect('/validate-email')

@users.route('/validate-email',methods=['POST'])
@login_required
def validation_route():
    user= User.get_one(session['user']['id'])
    if request.form['confirmation_hash'] != user.confirmation_hash:
        flash('Codigo incorrecto','error')
        return redirect('/validate-email')
    else: 
        flash('Cuenta verificada!','success')
        User.update_validated(session['user']['id'],1)
        if user.type == 1:
            return redirect('/dashboard')
        else:
            return redirect('/therapist-reg')

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
