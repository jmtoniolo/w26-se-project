# iOS - Inventory Optimization Software

DISCLAIMER: This code is provided "as is," with absolutely no warranty
expressed or implied. Any use of this software is at your own risk.

# Django Project Setup

## Prerequisites

-   **Python** (Verify with `python --version`)
-   **pip** (Verify with `pip --version`)

## Quick Start

### Set Up a Virtual Environment

It is best practice to run Django inside a virtual environment to manage
dependencies.

### Install and activate a virtual environment

``` powershell
python3 -m venv venv
source venv/bin/activate/Activate.ps1
```

### Install django in your venv

``` powershell
pip install django
```

### Run Database Migrations

This project uses Django migrations to manage database structure
changes.

Before starting the server (and after pulling changes that include new
migrations), run:

``` powershell
python manage.py makemigrations
python manage.py migrate
```

### Start Django server

cd into the project directory where manage.py is

``` powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/inventory_optimization_software/ with a web
browser!
