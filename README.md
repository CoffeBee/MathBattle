# MathBattle

## Installation

Installation requires installed python3 with pip and **postgres** on computer.

```bash
git clone https://github.com/CoffeBee/MathBattle.git
cd MathBattle
python3 -m pip install django==2.2.7 psycopg2 whitenoise python-memcached Pillow django-summernote django-user-agents
python3 -m pip install -e git://github.com/qcoumes/django-enumfields@6aa094ad1b6057b740fbf855ef50cf135e460ed9#egg=django_enumfields
```

Now you should open mathbattle/setting.py and edit database information:
```python
...
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME' : '<YOUR_DATABASE_NAME_HERE>',
       'USER' : '<YOUR_DATABASE_USERNAME_HERE>',
       'PASSWORD' : '<YOUR_DATABASE_PASSWORD_HERE>gres',
       'HOST' : '<YOUR_POSTGRES_HOST_HERE>',
       'PORT' : '<YOUR_POSTGRES_PORT_HERE>'

    }
}
...
```

After that you should create migrations and migrate them:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

And now you can run server
```bash
python3 manage.py runserver
```
