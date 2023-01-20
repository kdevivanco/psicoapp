from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.categories import Category
from app.models.therapists import Therapist
from app.decorators import login_required
from app.models.educations import Education
from app.models.users import User
import json
import pdb
import pprint

therapist = Blueprint('therapist', __name__, template_folder='templates')


#UPLOAD DE ARCHIVOS EN EL PERFIL DEL TERAPEUTA
#Ruta para cambiar la imagen desde el avatar (Decidir si este enlace lleva directamente o si llleva al perfil)
@therapist.route('/edit_pic')
# @login_required
def edit_pic():
    return render_template('add_picture.html')


@therapist.route('/edit_therapist/changeimg', methods = ['POST'])
def change_profile_img():
    file = request.files['file'] # Estamos accediendo al archivo cargado
    file.save('app/static/img/therapist/' + file.filename ) # Se guarda la imagen con el nombre original del archivo
    # accedemos al método en Therapist para agregarlo en la base de datos
    Therapist.set_profile_pic(
        session['user']['email'],   # Necesito sacar el email de la sesión
        file.filename
    )             # Necesito el nombre del archivo que llega
    session['user']['profile_pic'] = file.filename
    return redirect('edit_therapist_upload.html')
    # Faltaría guardar en session, la imagen para que siga apareciendo en la app cada vez que el usuario ingresa

# En el modelo de Therapist se creó un método para agregar la ruta en la basse de datos, del archivo que el usuario adjunta 



#PROTECCION DE RUTA PARA USUARIOS TERAPEUTAS Y DUENOS:
def therapist_protection(user_id):
    us_type = session['user']['type']
    sesus_id = session['user']['id']
    if us_type != 0 and sesus_id != user_id: #no es terapeuta
        flash('not allowed on this route!', 'error')
        return False

# Mostrar el registro de terapeuta
@therapist.route('/therapist-reg')
def show_therapist_register():
    user = User.get_one(session['user']['id'])
    if user.type == 0 and user.validated == 1: #Ha verificado su email pero no llenado info de psicologo
        #redirecionamos a terminar perfil
        return redirect('/therapist-reg')
    elif user.type == 0 and user.validated == 2:
        return redirect('/add-education')
    elif user.type == 0 and user.validated == 3: 
        return redirect(f'/tprofile/{user.id}')

    all_categories = Category.get_all()

    return render_template('reg_therapist.html', all_categories = all_categories)

@therapist.route('/therapist-reg', methods = ['POST'])
@login_required
def register_therapist():

    selected_categories = request.form.getlist('category')
    Therapist.fill_info(request.form,session['user']['id'])

    for cat_id in selected_categories:
        Category.add_to_category(session['user']['id'],int(cat_id))

    return redirect('/add-education')#/add-education.html'


@therapist.route('/add-education')
#@login_required
def show_add_education():
    therapist = Therapist.classify(session['user']['id'])
    return render_template('add_education.html', therapist = therapist)

@therapist.route('/education', methods = ['POST'])
#@login_required
def education_add():
    user_id = session['user']['id']
    Education.add_education(request.form,user_id)
    Therapist.update_validated('education',user_id)
    Education.get_education(user_id)
    
    return redirect(f'/tprofile/{user_id}')


# ENTRA AL PERFIL DEL TERAPEUTA
@therapist.route('/tprofile/<therapist_id>')
@login_required
def profile_therapist(therapist_id):
    logged = True
    therapist = Therapist.classify(therapist_id)
    for article in therapist.articles:
        print(article.img_filename)
        print(type(article.img_filename))
    pdb.set_trace()
    if therapist.type == 1:
        return redirect('/dashboard')
    user_id = session['user']['id']
    return render_template('profile_therapist.html',logged = logged, therapist = therapist,user_id = user_id)



# EDITA EL PERFIL DEL TERAPEUTA
@therapist.route('/edit-therapist')
def edit_therapist():
    user_id = session['user']['id']
    therapist = Therapist.classify(user_id)
    return render_template('edit_therapist.html',user_id= user_id, therapist = therapist)


# BUSCA UN TERAPEUTA
@therapist.route('/search_therapist')
def search_therapist():
    return render_template('search_therapist.html')