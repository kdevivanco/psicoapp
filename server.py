from app import app 

from app.controllers.users import users
from app.controllers.therapist import therapist
from app.controllers.publications import publications
from app.controllers.articles import articles 
<<<<<<< HEAD
from app.controllers.page import page
from app.controllers.patients import patients
=======
>>>>>>> 6553481ea2490fc488ad15a49d6dc7a250404d94
#from app.controllers.messages import messages

app.register_blueprint(users)
app.register_blueprint(therapist)
app.register_blueprint(publications)
app.register_blueprint(articles)
<<<<<<< HEAD
app.register_blueprint(page)
app.register_blueprint(patients)
=======
#app.register_blueprint(messages)
>>>>>>> 6553481ea2490fc488ad15a49d6dc7a250404d94



# if __name__ == "__main__":
#     app.run(debug=True)

# Nota para Kayla: copio este mismo que el anterior, pero con el puerto 8.000 porque por alguna razón en mi pc no funciona el otro
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)