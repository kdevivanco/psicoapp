from flask import request, redirect, render_template, Blueprint, flash, session
from app.models.users import User # Tengo que llamar al modelo donde tengo el método de cambiar el avatar
import pdb


routes = Blueprint('skeleton', __name__, template_folder='templates')


@routes.route('/register')
def show_register():
    return render_template('register_psicoapp.html')

@routes.route('/register',methods=["POST"])
def register_user():
    if not User.email_free(request.form):
        return redirect('/register')
    if not User.validate_user(request.form):
        return redirect('/register')
    
    password = User.encrypt_pass(request.form['password'])

    session['user'] = {
        'id': None,
        'email' : request.form['email'],
        'full_name' : request.form['full_name'],
        'password' : password,
        'account_type' : request.form['account_type']
    }
    print
    return redirect('/edit_therapist')


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


@routes.route('/edit_therapist/changeimg', methods = ['POST'])
def change_profile_img():
    pdb.set_trace()
    file = request.files['file'] # Estamos accediendo al archivo cargado
    file.save('app/static/img/users/' + file.filename ) # Se guarda la imagen con el nombre original del archivo
    # accedemos al método en user para agregarlo en la base de datos
    User.set_profile_pic(
        session['user']['email'],   # Necesito sacar el email de la sesión
        file.filename
    )             # Necesito el nombre del archivo que llega
    session['user']['profile_pic'] = file.filename
    return redirect('profile_therapist.html')
    # Faltaría guardar en session, la imagen para que siga apareciendo en la app cada vez que el usuario ingresa

# En users se creó un método para agregar la ruta en la basse de datos, del archivo que el usuario adjunta 



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
    return render_template('register_psicoapp.html')

# @routes.route('/register', methods = ['POST'])
# def create_user(cls,form_data):

#     query = '''
#             INSERT INTO users ( name , email , password , type, created_at ) 
#             VALUES ( %(name)s  , %(email)s , %(password)s , %(type)s, NOW());
#             '''

#     data = {
#             "name": form_data["name"],
#             "email" : form_data["email"],
#             "type" : form_data["type"],
#             "password" : password
#         }
    
    
#     flash('Register  succesful!','success')

#     connectToMySQL('psicoapp').query_db(query,data)
#     return render_template('register_psicoapp.html')


@routes.route('/search_therapist')
def search_therapist():
    return render_template('search_therapist.html')


@routes.route('/logout')
def logout():
    session['user'] = None
    return redirect('index.html')






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
