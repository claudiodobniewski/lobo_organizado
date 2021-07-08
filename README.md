# lobo_organizado
Gestion asociacion civil pequeña

## Dependencias

Desarrollado sobre 

* python 3.6 
instalado con pyp3 (pip para python 3)  

* django python 3.2.0

usar pip3.6 o pip3 segun ambientes

* django-bootstrap4
> pip3 install django-bootstrap4
> pip3 install django-bootstrap-icons https://pypi.org/project/django-bootstrap-icons/

> pip3 install django_material_icons https://icons.getbootstrap.com/

* crispy template tag library
> pip3 install django-crispy

# pythonanywhere

para mysql se requiere
> pip3 install mysqlclient

- On ubuntu require mibmysqlclient-dev first:
> sudo apt-get install libmysqlclient-dev
> pip3 install mysqlclient

Daba error no encontraba libreria dateutil
> pip install python-dateutil
## Comandos dentro de proyecto git "lobo_organizado"

Iniciar webserver dev python default port 8000
$ python3 manage.py runserver

puerto 8000
$python3 manage.py runserver 8080

intereface 0.0.0.0 puerto 8080
$ python3 manage.py runserver 0:8080

## Crear app en el proyecto

> python3 manage.py startapp nombreapp
## Migraciones

- Genera una migracion
$ python3 manage.py makemigrations socios
Migrations for 'socios':
  socios/migrations/0001_initial.py
    - Create model Familia
    - Create model Socio


- Ejecuta las migraciones de "socios"
$ python3 manage.py migrate socios
Operations to perform:
  Apply all migrations: socios
Running migrations:
  Applying socios.0001_initial... OK

- Ejecuta todas las migraciones
 $ python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, socios
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK

 ## API /Shell

  $ python3 manage.py shell

> from socios.models import Socio, Familia

> Socio.objects.all()
 <QuerySet []>

> familia1 = Familia(familia_crm_id="Dobniewski CSSJ",creado=timezone.now(),actualizado=timezone.now() )

> familia1

 <Familia: Familia object (None)>

> familia1.save()

> import datetime

> miembro1 = Socio(familia=familia, nombres="Claudio Javier",apellidos="Dobniewski", dni="22960795", fecha_nacimiento=datetime.datetime(1972, 9, 16),creado=timezone.now(),actualizado=timezone.now() )
> 
> miembro1.save()

## Superuser

> python3 manage.py createsuperuser
Username (leave blank to use 'claudio'): claudio
Email address: claudiojd@gmail.com
Password: 
Password (again): 
Superuser created successfully.

* Luego entrar en http://127.0.0.1:8000/admin/. y se accedera al portal de administracion

----------------------------------------------------------

# LOOK AND FEEL  - bootstrap4

* Instalar bootstrap 4
pip3 install django-bootstrap4

* Instalar bootstrap
pip3 install django-icons
https://readthedocs.org/projects/django-icons/downloads/pdf/latest/

--------------------------------------------------------------
> https://docs.djangoproject.com/en/3.2/topics/testing/overview/

# usar auditlog de django
##  dependencia 
> NO pip3 install six  <-- https://stackoverflow.com/questions/20741754/python-2-unicode-compatible-error
> NO pip3 install django-six <-- https://github.com/geex-arts/django-jet/issues/418
>  pip3 install django-utils-six <--  Y EJECUTAR migrate | https://github.com/jazzband/django-auditlog/issues/265
> pip3 install django-auditlog==1.0a1 <--- verion default 0.4 no funciona  https://django-auditlog.readthedocs.io/



# Run all the tests
$ python3 manage.py test
# Run all the tests in the animals.tests module
$ python3 manage.py test socios.tests

# Run all the tests found within the 'animals' package
$ python3 manage.py test socios

# Run just one test case
$ python3 manage.py test socios.tests.SocioTestCase

# Run just one test method
$ python3 manage.py test animals.tests.SocioTestCase.test_animals_can_speak

$ python3 manage.py test socios/tests/ --pattern="tests.py"


# Virtual env the
* source .virtualenvs/lobo_organizado-virtualenv/bin/activate

# Collect statics file compila los files staticos (assets de django) en un directorio para incluir en el proyecto
python3 manage.py collectstatic


