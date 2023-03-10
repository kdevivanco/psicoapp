from flask import Flask, render_template, request, redirect, Blueprint,session,flash
from app.models.categories import Category
from app.models.articles import Article
from app.models.users import User
from app.models.therapists import Therapist
from app.decorators import login_required
import json
import pdb
from app.models.confirmation_hash_test import generate_confirmation_hash
from datetime import datetime
import locale





articles = Blueprint('articles', __name__, template_folder='templates')

def check_logged():
    if 'user' not in session or session['user'] == None:
        return False
    else:
        return True

@articles.route('/add_article')
@login_required
def show_add_article():
    logged = True
    user = User.get_one(session['user']['id'])
    therapist = Therapist.classify(session['user']['id'])
    if user.type == 1: #es paciente
        flash('Usted no tiene permiso para acceder a esta ruta', 'error')
        return redirect('/dashboard')
    if therapist.validated != 3:
        flash('Falta que termines de completar tu perfil','error')
        return redirect('/therapist-reg')
    return render_template('add_article.html',user=user,logged=logged)

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
    
    return redirect(f'/tprofile/{user_id}')

@articles.route('/article/<id>')
def show_article(id):
    logged = check_logged()
    user = None
    if logged == True:
        user = User.get_one(session['user']['id'])

    article = Article.classify(id)
    author = Therapist.classify(article.user_id)
    date_string = article.created_at
    date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    date = date_object.strftime("%A %d de %B de %Y")

    return render_template('article.html', article = article, author = author, logged = logged, user = user,date= date)

@articles.route('/edit-article/<id>')
@login_required
def show_edit(id):
    user = User.get_one(session['user']['id'])
    logged = True
    article = Article.classify(id)
    author = Therapist.classify(article.user_id)
    if author.id != session['user']['id']:
        flash("Lo sentimos, no est??s autorizado para realizar esta acci??n",'error')
        return redirect('/')
    body = article.body.replace('<br>','')
    return render_template('edit_article.html', article = article, author = author,body = body, user=user, logged = logged)


@articles.route('/edit-art/<int:id>/editado', methods = ['POST'])
def edited_article(id):
    Article.save_edited_article(request.form, id)
    print(session['user']['id'])
    return redirect(f"/tprofile/{session['user']['id']}")



    #ruta post edit - article
    #actualizar Article.update(form,articleid)
