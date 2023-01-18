from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.categories import Category
from app.models.therapists import Therapist
from app.decorators import login_required
import json
import pdb

therapist = Blueprint('therapist', __name__, template_folder='templates')



# ENTRA AL PERFIL DEL TERAPEUTA
@therapist.route('/tprofile/<id>')
@login_required
def profile_therapist(id):
    
    return render_template('profile_therapist.html')



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