from app import app 

from app.controllers.users import users
from app.controllers.therapist import therapist
from app.controllers.publications import publications
from app.controllers.articles import articles 
from app.controllers.page import page
from app.controllers.patients import patients
#from app.controllers.messages import messages

app.register_blueprint(users)
app.register_blueprint(therapist)
app.register_blueprint(publications)
app.register_blueprint(articles)
app.register_blueprint(page)
app.register_blueprint(patients)
#app.register_blueprint(messages)



# if __name__ == "__main__":
#     app.run(debug=True)

# Nota para Kayla: copio este mismo que el anterior, pero con el puerto 8.000 porque por alguna razón en mi pc no funciona el otro
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)