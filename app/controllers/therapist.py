from flask import Flask, render_template, request, redirect, Blueprint, session, flash
from app.models.categories import Category
from app.models.therapists import Therapist
from app.models.users import User
from app.decorators import login_required
from app.models.educations import Education
from app.models.locations import Location
from app.models.messages import Message
from app.models.users import User
from app.models.confirmation_hash_test import generate_confirmation_hash
import json
import pdb
import pprint

therapist = Blueprint('therapist', __name__, template_folder='templates')


# UPLOAD DE ARCHIVOS EN EL PERFIL DEL TERAPEUTA
# Ruta para cambiar la imagen desde el avatar (Decidir si este enlace lleva directamente o si llleva al perfil)
@therapist.route('/edit_pic')
# @login_required
def edit_pic():
    return render_template('add_picture.html')


# @therapist.route('/therapist_edited', methods=['POST'])
# def change_profile_img():
#     user_id = session['user']['id']
#     file = request.files['file']  # Estamos accediendo al archivo cargado
#     img_hash = generate_confirmation_hash(file.filename) #importar generate_confirmation_hash()

#     file.filename = f'profile-{img_hash}-{user_id}.png'
#     file.save('app/static/img/therapist/' + file.filename)
#     print(request)

#     Therapist.set_profile_pic(
#         session['user']['email'], 
#         file.filename
#     )            
#     session['user']['profile_pic'] = file.filename
#     return redirect(f"/tprofile/{session['user']['id']}")




# PROTECCION DE RUTA PARA USUARIOS TERAPEUTAS Y DUENOS:
def therapist_protection(user_id):
    us_type = session['user']['type']
    sesus_id = session['user']['id']
    if us_type != 0 and sesus_id != user_id: #no es terapeuta
        flash('not allowed on this route!', 'error')
        return False

# Mostrar el registro de terapeuta
@therapist.route('/therapist-reg')
@login_required
def show_therapist_register():
    logged = True
    user = User.get_one(session['user']['id'])
    all_cities = Location.get_all()

    all_categories = Category.get_all()
    if user.validated == 0:
        return redirect('/validate-email')
    if user.type == 0 and user.validated == 1: #Ha verificado su email pero no llenado info de psicologo
        # redirecionamos a terminar perfil
        return render_template('reg_therapist.html', all_categories = all_categories, all_cities = all_cities, logged=logged,user = user)
    elif user.type == 0 and user.validated == 2:
        return redirect('/add-education')
    elif user.type == 0 and user.validated == 3: 
        return redirect(f'/tprofile/{user.id}')

    return render_template('reg_therapist.html', all_categories = all_categories, all_cities = all_cities, logged=logged,user = user)

@therapist.route('/therapist-reg', methods = ['POST'])
@login_required
def register_therapist():
    

    selected_categories = request.form.getlist('category')
    Therapist.fill_info(request.form,session['user']['id'])

    for cat_id in selected_categories:
        Category.add_to_category(session['user']['id'],int(cat_id))

    return redirect('/add-education')#/add-education.html'


@therapist.route('/add-education')
@login_required
def show_add_education():
    user = User.get_one(session['user']['id'])
    logged = True
    therapist = Therapist.classify(session['user']['id'])
    return render_template('add_education.html', therapist = therapist,user=user,logged=logged)

@therapist.route('/education', methods = ['POST'])
# @login_required
def education_add():
    user_id = session['user']['id']
    Education.add_education(request.form,user_id)
    Therapist.update_validated('education',user_id)
    Education.get_education(user_id)
    
    return redirect(f'/tprofile/{user_id}')


# ENTRA AL PERFIL DEL TERAPEUTA
@therapist.route('/tprofile/<therapist_id>')
def profile_therapist(therapist_id):
    this_user = User.get_one(therapist_id)
    if this_user.validated < 2:
        flash('Debe terminar la validacion de registro','error')
        return redirect('/therapist-reg')

    therapist = Therapist.classify(therapist_id)
    recieved_messages = []
    if 'user' not in session or session['user']==None:
        user = None
        logged = False
    else:
        logged = True
        user = User.get_one(session['user']['id'])
        if therapist.id == user.id:
            recieved_messages = Message.get_recieved(session['user']['id'])
            for message in recieved_messages:
                if message.status == 'deleted':
                    recieved_messages.remove(message)

    for article in therapist.articles:
        print(article.img_filename)
        print(type(article.img_filename))
    


    return render_template('profile_therapist.html',logged = logged, therapist = therapist,user = user, recieved_messages = recieved_messages)


@therapist.route('/add-district')
@login_required
def show_add_district():
    logged = True
    user = User.get_one(session['user']['id'])
    if user.type == 1:
        return redirect('/dashboard')
    locations = Location.city_districts(user.city)

    return render_template('add_district.html',logged=logged, user=user,locations = locations)

@therapist.route('/add-district', methods=['POST'])
def add_district():
    user_id = session['user']['id']
    location_id = request.form['location_id']
    Location.log_location(location_id,user_id)

    return redirect(f'/tprofile/{user_id}')

# # BUSCA UN TERAPEUTA
# @therapist.route('/show-search')
# def show_search():
#     return render_template('search_therapist.html')

# EDITA EL PERFIL DEL TERAPEUTA
@therapist.route('/edit-therapist')
@login_required
def edit_therapist():
    this_user = User.get_one(session['user']['id'])
    if this_user.validated < 2:
        flash('Debe terminar la validacion de registro','error')
        return redirect('/therapist-reg')
    logged = True
    user_id = session['user']['id']
    therapist = Therapist.classify(user_id)
    user = therapist
    return render_template('edit_therapist.html',user_id= user_id, therapist = therapist,user = user, logged = logged)


@therapist.route('/therapist_edited', methods = ['POST'])
@login_required
def save_therapist_edited():
    user_id = session['user']['id']
    file = request.files['file']  
    img_hash = generate_confirmation_hash(file.filename) 

    file.filename = f'profile-{img_hash}-{user_id}.png'
    file.save('app/static/img/therapist/' + file.filename)

    file_path = f'/img/therapist/{file.filename}'
    # Therapist.set_profile_pic(
    #     session['user']['email'], 
    #     file.filename
    # )            
    Therapist.save_therapist_edited(request.form, user_id, file_path)
    return redirect(f"/tprofile/{session['user']['id']}")
