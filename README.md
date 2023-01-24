# Psicoapp
## Esta app se crea con el objetivo de que las personas del común, tengan la oportunidad de crear red con varios psicólogos de su interés e incluso tener contacto con ellos antes de agendar una cita, lo que aumenta las probabilidades de procesos más exitosos, considerando que el cuidado de la salud mental es uno de los pilares fundamentales del bienestar humano.Adicionalmente, los psicólogos pueden hacer red entre ellos para complementar sus métodos y actualizarse

## IMPORTANTE! Para correr el app con verificación de email, poner su gmail y app pasword en la funcion ""send_confirmation_email"" del modelo ""confirmation_hash_test.py"" y en elm metodo "send_confirmation_email" del modelo users.py, si no, usar el commit anterior


### Requerimientos:

Python==3.8 en adelante
Flask==1.1.2
Flask_Bcrypt==1.0.1
PyMySQL==1.0.2

Pasos para instalar y ejecutar la aplicación.

Asumiendo que el ejecutable de python es "python3":

1. Instalar el Ambiente Virtual:

python3 -m venv mi_env


2. Activar el Ambiente Virtual:

source mi_env/bin/activate


3. Instalar las bibliotecas usadas en Python:

pip install flask, flask_bcrypt, pymysql


El servidor se accede por el puerto 8000:
http://localhost:8000


4. Instalar requerimientos en el ambiente virtual: 


5. Ejecutar la app:

    python3 server.py (para MACS)
    python server.py (para windows)
