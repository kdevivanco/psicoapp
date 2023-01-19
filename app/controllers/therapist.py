from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.categories import Category
from app.models.therapists import Therapist
from app.decorators import login_required
import json
import pdb
import pprint

therapist = Blueprint('therapist', __name__, template_folder='templates')


#PROTECCION DE RUTA PARA USUARIOS TERAPEUTAS Y DUENOS:
def therapist_protection(user_id):
    us_type = session['user']['type']
    sesus_id = session['user']['id']
    if us_type != 0 and sesus_id != user_id: #no es terapeuta
        flash('not allowed on this route!', 'error')
        return False

# TERMINAR EL REGISTRO DEL TERAPEUTA 
@therapist.route('/therapist-reg')
def show_therapist_register():
    
    all_categories = Category.get_all()

    return render_template('reg_therapist.html', all_categories = all_categories)

@therapist.route('/therapist-reg', methods = ['POST'])
def register_therapist():

    selected_categories = request.form.getlist('category')
    Therapist.fill_info(request.form,session['user']['id'])

    for cat_id in selected_categories:
        Category.add_to_category(session['user']['id'],int(cat_id))

    return redirect('/add-education')#/add-education.html'


@therapist.route('/add-education')
@login_required
def show_add_education():
    return render_template('add_education.html')



# ENTRA AL PERFIL DEL TERAPEUTA
@therapist.route('/tprofile/<id>')
@login_required
def profile_therapist(id):
    logged = True
    return render_template('profile_therapist.html',logged = logged)



# EDITA EL PERFIL DEL TERAPEUTA
@therapist.route('/edit_therapist/<id>')
def edit_therapist():
    return render_template('edit_therapist.html')



#UPLOAD DE ARCHIVOS EN EL PERFIL DEL TERAPEUTA
@therapist.route('/edit_therapist/changeimg', methods = ['POST'])
def change_profile_img():
    # pdb.set_trace()
    file = request.files['file'] # Estamos accediendo al archivo cargado
    file.save('app/static/img/therapist/' + file.filename ) # Se guarda la imagen con el nombre original del archivo
    # accedemos al método en user para agregarlo en la base de datos
    Therapist.set_profile_pic(
        session['user']['email'],   # Necesito sacar el email de la sesión
        file.filename
    )             # Necesito el nombre del archivo que llega
    session['user']['profile_pic'] = file.filename
    return redirect('profile_therapist.html')
    # Faltaría guardar en session, la imagen para que siga apareciendo en la app cada vez que el usuario ingresa

# En el modelo de Therapist se creó un método para agregar la ruta en la basse de datos, del archivo que el usuario adjunta 



# BUSCA UN TERAPEUTA
@therapist.route('/search_therapist')
def search_therapist():
    return render_template('search_therapist.html')