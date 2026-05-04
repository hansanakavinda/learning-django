# learning-django

### create project

'''
django-admin startproject <project_name>
cd <project_name>
'''

### create app

'''
python manage.py startapp <app_name>
'''

then add the project name to the settings.py to the INSTALLED_APPS list

### run development server

'''
python manage.py runserver
'''

### make model changes

'''
python manage.py makemigrations
python manage.py migrate
'''

### create admin user

'''
python manage.py createsuperuser
'''

### shell running database queries

'''
python manage.py shell
'''