from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.categories import Category
from app.models.articles import Article
import json
import pdb


articles = Blueprint('articles', __name__, template_folder='templates')


@articles.route('/add_article')
def add_article():
    return render_template('add_article.html')