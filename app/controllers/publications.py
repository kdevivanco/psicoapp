from flask import Flask, render_template, request, redirect, Blueprint,session,flash
from app.models.categories import Category
from app.models.publications import Publication
from app.models.users import User
from app.models.therapists import Therapist
from app.decorators import login_required
from app.models.confirmation_hash_test import generate_confirmation_hash
import json
import pdb


publications = Blueprint('publications', __name__, template_folder='templates')


@publications.route('/add_publication')
@login_required
def show_add_publication():
    user = User.get_one(session['user']['id'])
    therapist = Therapist.classify(session['user']['id'])
    if user.type == 1: #es paciente
        flash('Usted no tiene permiso para acceder a esta ruta', 'error')
        return redirect('/dashboard')
    if therapist.validated != 3:
        flash('Falta que termines de completar tu perfil','error')
        return redirect('/therapist-reg')
    logged = True
    return render_template('add_publication.html', user=user, logged = logged)


@publications.route('/add-publication', methods = ['POST'])
def add_publication():
    file_name = request.files['file'].filename
    if file_name[-4:] != ".pdf":
        flash('ONLY PDFS ARE ACCEPTED!','error')
        return redirect('/add_publication')

    user_id = session['user']['id']
    file = request.files['file'] # Estamos accediendo al archivo cargado
    file_hash = generate_confirmation_hash(file.filename) #importar generate_confirmation_hash()
    file.filename = f'article-{file_hash}-{user_id}.pdf'
    file.save('app/static/pdf/publications/' + file.filename) 
    file_name = file.filename
    pdb.set_trace()
    Publication.create(file_name,request.form,int(session['user']['id']))
    
    user = User.get_one(session['user']['id'])
    if user.type == 1: #es paciente
        flash('Usted no tiene permiso para acceder a esta ruta', 'error')
        return redirect('/dashboard')
    return render_template('add_publication.html')