# learning-django

### create project

. after the "project name" tells django to use the current directory as the project root or else it creates one

```
django-admin startproject <project_name> .
cd <project_name>
```

### create app

```
python manage.py startapp <app_name>
```

then add the project name to the settings.py to the INSTALLED_APPS list

### run development server

can pass a port number which is optional

```
python manage.py runserver <port>
```

### make model changes

```
python manage.py makemigrations
python manage.py migrate
```

### create admin user

```
python manage.py createsuperuser
```

### shell running database queries

```
python manage.py shell
```