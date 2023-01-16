from flask import request, redirect, render_template, Blueprint, flash, session


routes = Blueprint('skeleton', __name__, template_folder='templates')


@routes.route('/home')
def home():
    return render_template('index.html')


@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/add_article')
def add_article():
    return render_template('add_article.html')


@routes.route('/add_publication')
def add_publication():
    return render_template('add_publication.html')


@routes.route('/edit_therapist')
def edit_therapist():
    return render_template('edit_therapist.html')


@routes.route('/edit_user')
def edit_user():
    return render_template('edit_user.html')


@routes.route('/ini_sesion')
def ini_sesion():
    return render_template('ini_sesion.html')


@routes.route('/profile_therapist')
def profile_therapist():
    return render_template('profile_therapist.html')


@routes.route('/profile_user')
def profile_user():
    return render_template('profile_user.html')


@routes.route('/register')
def register():
    return render_template('register.html')


@routes.route('/search_therapist')
def search_therapist():
    return render_template('search_therapist.html')





# @skeleton.route('/suscribe', methods=['POST'])
# def suscribe():
#     # 0. Validar el formulario
#     if not Suscribe.validate(request.form):
#         return redirect('/home')

#     # 1. Registrar el email
#     Suscribe.insert_new_email(request.form['email'])
#     flash('Hemos registrado tu correo electrónico con éxito', 'success')
#     return redirect('/home')


    
# @skeleton.route('/map')
# def map():
#     return render_template('map.html')


# @skeleton.route('/nextevents')
# def next_events():
#     return render_template('events.html')


# @skeleton.route('/about')
# def about():
#     return render_template('about.html')


# @skeleton.route('/shows')
# def shows():
#     return render_template('shows.html')


# @skeleton.route('/hireus')
# def hireus():
#     return render_template('hireus.html')


# @skeleton.route('/contactus')
# def contactus():
#     return render_template('contact.html')

# @skeleton.route('/admin')
# def admin():
#     SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#     SAMPLE_SPREADSHEET_ID = '10jIqqAkI95GfwCKoOzF0nCSou1p69G4U-N2rnoHo_Zc'
#     data = SaveGoogleSheetsdata(SCOPES, SAMPLE_SPREADSHEET_ID)
#     data.get_data_google_sheets()
#     return redirect('/home')
