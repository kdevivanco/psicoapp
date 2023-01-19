from flask import Flask, render_template, request, redirect, Blueprint,session,flash
from app.models.categories import Category
from app.models.publications import Publication
from app.models.users import User
from app.decorators import login_required
import json
import pdb


publications = Blueprint('publications', __name__, template_folder='templates')


@publications.route('/add_publication')
def add_publication():
    user = User.get_one(session['user']['id'])
    if user.type == 1: #es paciente
        flash('Usted no tiene permiso para acceder a esta ruta', 'error')
        return redirect('/dashboard')
    return render_template('add_publication.html')