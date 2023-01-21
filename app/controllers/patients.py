from flask import Flask, render_template, request, redirect, Blueprint,session,flash
from app.models.categories import Category
from app.models.users import User
from app.decorators import login_required
from app.models.locations import Location
import json
import pdb
import pprint

patients = Blueprint('patients', __name__, template_folder='templates')

def permiso_paciente():
    user = User.get_one(session['user']['id'])
    if user.type == 1: #es paciente
        return True
    else:
        flash('Usted no tiene permiso para acceder a esta ruta', 'error')
        return False 

# TERMINAR EL REGISTRO DEL Paciente 
@patients.route('/patient-reg')
def show_patient_register():
    if permiso_paciente() != True:
        return redirect('/dashboard')
    user = User.get_one(session['user']['id'])
    all_categories = Category.get_all()
    all_cities = Location.get_all()

    return render_template('reg_user.html', all_categories = all_categories, all_cities = all_cities)


@patients.route('/patient-reg', methods = ['POST'])
def fill_info():
    if not permiso_paciente():
        return redirect('/dashboard')

    User.fill_info_patient(request.form,session['user']['id'])
    
    selected_categories = request.form.getlist('category')

    for cat_id in selected_categories:
        Category.add_to_category(session['user']['id'],int(cat_id))

    return redirect('/dashboard')

# # TERMINAR EL REGISTRO DEL TERAPEUTA 
# @patients.route('/patient-reg', methods="POST")
# def fill_patient_info():
#     # user = User.get_one(session['user']['id'])
#     all_categories = Category.get_all()

#     return render_template('reg_user.html', all_categories = all_categories)