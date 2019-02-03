# Proce

A simple web application to manager processes. 

Link of the running project: https://proce.cloudatlas.org/


## Features

- Django 2.1+
- Development, Staging and Production settings with [python-decouple](https://pypi.org/project/python-decouple/)
- Get value insight and debug information while on Development with [django-debug-toolbar](https://django-debug-toolbar.readthedocs.org).
- Create fake data with [model-mommy](https://model-mommy.readthedocs.io/en/latest/basic_usage.html) 
- Frontend using django templates + framework css with [Semantic-ui](https://semantic-ui.com/) + DOM manipulation with [Jquery3](http://api.jquery.com/)
- Color palette available at: /static/core/palette.pdf


## Requirements

- Python >= 3.6


## How to configure and run the project

> Remember to create a new virtualenv first


```bash
$ git clone git@github.com:marcosflp/process_manager.git
$ cd process_manager
$ pip install -r requirements.txt
```

##### Custom django settings

You must create a settings.ini file at the root of the project. To create this file, use the settings.ini.example template.

```
$ cp settings.ini.example settings.ini 
```

These settings(and their default values) are used on development, staging or production environments.

> You don't need to change the the settings to run the project.

Default settings that you can change on the settings.ini file.
```
DEBUG=True
SECRET_KEY=4cn68iga94@**2x9vb1f*-104pe%%*-u-%%#%%1wh!r(+mjiza@y$
ENVIRONMENT_MODE='dev'  # 'dev' or 'prod' or 'test'

# Database
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_HOST=localhost
DATABASE_NAME=process_manager.sqlite3
DATABASE_USER=
DATABASE_PASSWORD=

# Logging
ENABLE_LOGGING=True

# Debug Toolbar
ENABLE_DEBUG_TOOLBAR=False
```


##### Running migration and create a superuser to access the system

```bash
$ python manage.py migrate
$ python manage.py createsuperuser
```


##### Running the project

```bash
$ python manage.py runserver
```


## Running the tests

```bash
$ python manage.py test
```
