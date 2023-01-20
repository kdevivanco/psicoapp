from flask import Flask, render_template, request, redirect, Blueprint,session,flash
from app.models.categories import Category
from app.models.articles import Article
from app.models.users import User
from app.models.therapists import Therapist
from app.decorators import login_required
import json
import pdb
from app.models.confirmation_hash_test import generate_confirmation_hash

articles = Blueprint('articles', __name__, template_folder='templates')

def check_logged():
    if 'user' not in session or session['user'] == None:
        return False
    else:
        return True

@articles.route('/add_article')
@login_required
def show_add_article():
    user = User.get_one(session['user']['id'])
    therapist = Therapist.classify(session['user']['id'])
    if user.type == 1: #es paciente
        flash('Usted no tiene permiso para acceder a esta ruta', 'error')
        return redirect('/dashboard')
    if therapist.validated != 3:
        flash('Falta que termines de completar tu perfil','error')
        return redirect('/therapist-reg')
    return render_template('add_article.html')

@articles.route('/add-article', methods=['POST'])
@login_required
def add_article():
    user_id = session['user']['id']

    file = request.files['file'] # Estamos accediendo al archivo cargado

    img_hash = generate_confirmation_hash(file.filename) #importar generate_confirmation_hash()

    file.filename = f'article-{img_hash}-{user_id}.png'

    file.save('app/static/img/articles/' + file.filename) 

    file_name = file.filename

    Article.create(file_name,request.form,int(session['user']['id']))
    
    return render_template('add_article.html')

@articles.route('/article/<id>')
def show_article(id):
    logged = check_logged()
    if logged == True:
        user = User.get_one(session['user']['id'])

    article = Article.classify(id)
    author = Therapist.classify(article.user_id)
    return render_template('article.html', article = article, author = author, logged = logged, user = user)

@articles.route('/edit-article/<id>')
@login_required
def show_edit(id):
    article = Article.classify(id)
    if article.creator.id != session['user']['id']:
        #flash
        return redirect('/')

    return render_template('edit_article.html', article = article)

    #ruta post edit - article
    #actualizar Article.update(form,articleid)
