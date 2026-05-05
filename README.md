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

- makemigrates & migrate
    - can pass "app_name" as optional parameter

- migrate
    - can pass --database="dbname" when working with multiple databases

```
python manage.py makemigrations <app_name>
python manage.py migrate <app_name> --database=<dbname>
```

### create admin user

```
python manage.py createsuperuser
```

### shell running database queries

```
python manage.py shell
```