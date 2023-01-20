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
@login_required
def add_publication():

    #Verificacion de pdf
    file_name = request.files['file'].filename
    if file_name[-4:] != ".pdf":
        flash('ONLY PDFS ARE ACCEPTED!','error')
        return redirect('/add_publication')
    
    #Creacion de nombre del archivo
    user_id = session['user']['id']
    file = request.files['file'] 
    file_hash = generate_confirmation_hash(file.filename) 
    title_hash = generate_confirmation_hash(request.form['title'])
    file.filename = f'publication{file_hash}{title_hash}{user_id}.pdf'
    file.save('app/static/pdfs/' + file.filename) 
    file_name = file.filename

    #Creacion de la publicacion en la base de datos
    pdb.set_trace()
    publication = Publication.create(file_name,request.form,int(session['user']['id']))
    pdb.set_trace()
    return redirect(f'/tprofile/{user_id}')


@publications.route('/publication/<id>')
def show_publication(id):
    publication = Publication.classify(id)
    if 'user' not in session or session['user'] == None:
        logged = False
        user = None
    
    logged = True
    user = User.get_one(session['user']['id'])

    return render_template('publication.html',publication = publication, user=user, logged = logged)