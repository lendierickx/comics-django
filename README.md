# comicscantina-django
## Description
A web-platform for distrubting online comic books.

## Features
* View all comics from Grand Comics Database
* Physical comic book inventory tracking system
* Print and track sales with QR codes
* Integrates with point of sales devices
* Digital comic book marketplace
* Online comics distribution

## System Requirements
* Python 3.4.x+
* Postgres SQL DB 9.4+
* pip 6.1.1+
* virtualenv 12.1.1+

## Build Instructions
### Application
For Linux and OSX users, run these commands:

1. First clone the project locally and then go into the directory

  ```
  git clone git@gitlab.com:theshootingstarpress/comicscantina-django.git
  cd comicscantina-django
  ```


2. Setup our virtual environment

  ```
  (OSX)
  python3 -m venv env

  (Linux)
  virtualenv env
  ```


3. Now lets activate virtual environment

  ```
  source env/bin/activate
  ```


4. OSX USERS ONLY: If you are using ‘Postgres.app’, you’ll need to have pg_config setup in your $PATH. If you already have set this up, skip this step, else simply run this command in the console to set the path manually.

  ```
  export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"
  ```


5. Now lets install the libraries this project depends on.

  ```
  pip install -r requirements.txt
  ```


### Database
We are almost done! Just follow these instructions and the database will be setup for the application to use.

1. Load up your postgres and enter the console. Then to create our database, enter:

  ```
  # create database ecantina_db;
  ```


2. To confirm it was created, run this line, you should see the database in the output

  ```
  # \l
  ```


3. Enter the database

  ```
  # \c ecantina_db
  ```


4. If you haven’t created an administrator for your previous projects, create one now by entering:

  ```
  # CREATE USER django WITH PASSWORD '123password';
  # GRANT ALL PRIVILEGES ON DATABASE ecantina_db to django;
  ```


5. Your database "ecantina_db" is now setup with an admin user account "django" using the passowrd "123password”.

### Application + Database
Run the following command to create your custom settings instance. Note: Please write all your application passwords here as it won't be tracked on git.

  ```
  $ cd ecantina_project/ecantina_project
  $ cp secret_settings_example.py secret_settings.py
  ```


Run the following commands to populate the database.
  ```
  $ cd ../ecantina_project
  $ python manage.py makemigrations
  $ python manage.py migrate
  $ python manage.py setup_ecantina
  ```



### Importing Grand Comics Database
Please see the file [gcd.txt](https://github.com/rodolfomartinez/comicscantina-django/blob/master/docs/manual/development/gcd.txt) for more instructions.

## Usage
To run the web-app, you’ll need to run the server instance and access the page from your browser.

Start up the web-server:

  ```
  $ cd ecantina_project
  $ python manage.py runserver
  ```


In your web-browser, load up the following url

  ```
  http://127.0.0.1:8000/
  ```


Congratulations, you are all setup to run the web-app! Have fun coding!
