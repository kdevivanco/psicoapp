from app import app 

from app.controllers.users import users
from app.controllers.publications import publications
from app.controllers.articles import articles 
from app.controllers.messages import messages

app.register_blueprint(users)
app.register_blueprint(publications)
app.register_blueprint(articles)
app.register_blueprint(messages)



if __name__ == "__main__":
    app.run(debug=True)