# Django Project Setup

## Prerequisites
* **Python** (Verify with `python --version`)
* **pip** (Verify with `pip --version`)

## Quick Start

### Set Up a Virtual Environment
It is best practice to run Django inside a virtual environment to manage dependencies.

### Install and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

python -m venv venv
venv\Scripts\activate

pip install django

python manage.py runserver

Common Commands
python manage.py startapp <name>,Creates a new Django app within the project.
python manage.py makemigrations,Prepares changes to your models for the database.
python manage.py migrate,Applies the changes to the database.
python manage.py createsuperuser,Creates an admin account for the /admin panel.
