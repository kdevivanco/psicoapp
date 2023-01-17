# psicoapp
Requerimientos para correr la aplicacion:

Python==3.8 en adelante
Flask==1.1.2
Flask_Bcrypt==1.0.1
PyMySQL==1.0.2

Para activar el ambiente virtual:
1. Crear ambiente virtual si no esta creado: 
    
    python3 -m venv mi_env

2. Activar ambiente virtual en carpeta belt_exam:

    source mi_env/bin/activate 

3. Cambiar al directorio de la aplicacion: 

    cd wishlist

4. Instalar requerimientos en el ambiente virtual: 

    pipenv install flask
    pipenv install pymysql
    pipenv install flask-bcrypt 
    pipenv install flask-reuploaded (NO SE TERMINO USANDO, QUEDA PARA SEGUNDA FASE)
    pipenv install flask-wtf (NO SE TERMINO USANDO, QUEDA PARA SEGUNDA FASE)


5. Correr app:

    python3 server.py (para MACS)
    python server.py (para windows)
