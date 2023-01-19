from flask import Flask, render_template, request, redirect, Blueprint,session,flash
from app.models.categories import Category
from app.models.articles import Article
from app.models.users import User
from app.models.therapists import Therapist
from app.decorators import login_required
import json
import pdb


articles = Blueprint('articles', __name__, template_folder='templates')


@articles.route('/add_article')
@login_required
def add_article():
    user = User.get_one(session['user']['id'])
    therapist = Therapist.classify(session['user']['id'])
    if user.type == 1: #es paciente
        flash('Usted no tiene permiso para acceder a esta ruta', 'error')
        return redirect('/dashboard')
    if therapist.validated != 3:
        flash('Falta que termines de completar tu perfil','error')
        return redirect('/therapist-reg')
    return render_template('add_article.html')