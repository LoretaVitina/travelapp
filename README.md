# travelapp

## actions with environment

```bash
# creation of environment
python3 -m venv travelapp-env

# activation of environment
source travelapp-env/bin/activate

# deactivation of environment
deactivate
```

## project creation

```bash
# install django
pip install --upgrade pip
pip install django
pip install requests

# create app
django-admin startproject travel_app
```

## app creation

```bash
# creating an app
python manage.py startapp journey
```

## actions with application

```bash
# starting server
GOOGLE_MAPS_APIKEY=apikeyhere python3 manage.py runserver

# database migration
python3 manage.py migrate

python3 manage.py makemigrations journey

# creation of admin user
python3 manage.py createsuperuser

```