from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.categories import Category
from app.models.publications import Publication
import json
import pdb


publications = Blueprint('publications', __name__, template_folder='templates')


@publications.route('/add_publication')
def add_publication():
    return render_template('add_publication.html')