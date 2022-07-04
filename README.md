# TIVIX Family Budget App

# About this app

This app was created using the following tech stack:

* Python 3.9
* Django 4.0.5
* Django REST FRAMEWORK 3.13.1
* SQLite3 (sticking to it was a deliberate decision to simplify the process of building the app in the local environment)

Authorization package [`dj-rest-auth`](https://dj-rest-auth.readthedocs.io/en/latest/) was used to provide all necessary authorization features

# Build using docker
In order to run this app using docker paste this command when in the project's directory
```
docker-compose up --build
```

# Run locally

Since this is a Django app, there're several steps that are needed to run it locally:

1. Install python 3.9 or newer
2. Clone the project to your machine
3. Enter the project's directory and create virtualenv e.g
   ```
   python3 -m virtualenv env
   or
   python3 -m venv env
   ```
4. Activate virtualenv
   
   ```
   (On linux)
   sourve env/bin/activate
   (On Windows)
   source env/Scripts/activate
   ```
5. Install project's dependencies
   ```
   pip install -r requirements.txt
   ```
6. Run the application:
   ```
   python3 manage.py migrate
   python3 manage.py runserver
   ```
7. Open your browser on http://localhost:8000/

# Run tests

```
pytest -vv
```
