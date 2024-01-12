Backend de la aplicación realizada con Flask-Restx y SQLAlchemy

Para ejecutar primero hay que instalar los paquetes:
pip install -r requirements.txt

Para crear la base de datos:
python manage.py crear

Para recrear la base de datos:
python manage.py recrear

Para crear datos necesarios para empezar:
python manage.py rellenar

Después ejecutar:
python manage.py run