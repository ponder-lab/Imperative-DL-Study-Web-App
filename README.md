# Imperative-DL-Study-Web-App
![Django CI](https://github.com/ponder-lab/Imperative-DL-Study-Web-App/actions/workflows/django.yml/badge.svg)

Web App for the Imperative DL Study
https://tranquil-anchorage-16644-bbe77c4a9151.herokuapp.com/

## Setup/Run Instructions
### Pre-requisites

#### Version Requirements
```aiignore
Python 3.13.1
Pip: 3.13
Django: 5.1.4
```
- Ensure Django is set up: https://docs.djangoproject.com/en/5.1/topics/install/
- For MySQL databases, ensure mysql is set up: https://dev.mysql.com/doc/refman/8.0/en/installing.html
    - Additionally, also ensure `mysqlclient` is installed (either via Brew or other methods) https://pypi.org/project/mysqlclient/
    - Ensure the below PATH is exported in your environment `export DYLD_LIBRARY_PATH="/usr/local/mysql/lib/"`
- For PostgreSQL databases, `pip install psycopg2-binary`

### Run Instructions
1) Ensure all pre-requisites above are met.
2) Install dependencies: `pip install -r requirements.txt`
3) Ensure database is set up correctly (both remote and local as needed), see instructions below.
4) Run the app: `python manage.py runserver`
   5) To enable debugging mode, export env variable: `export DJANGO_DEBUG="True"`
5) Navigate to: `localhost:8000` to view the app.
6) To create an admin account, `python manage.py createsuperuser` and follow instructions to provide account credentials.

- Debug: If the above `localhost:8000` page throws an access error, consider adding `localhost` to `ALLOWED_HOSTS` in the `settings.py` file.
- Debug: If you run into error regarding `STATIC_ROOT` see: https://github.com/OpenToAllCTF/OTA-University/issues/9 suggestion to change `STATIC_ROOT` assignment to just `/static/`

### Connect to a database
1) Create a database and configure the `DATABASES` dictionary in the `settings.py` file to connect to it.
   2) See steps below to set up a local database if needed.
2) Run migrations to create the schema using the commands:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
3) Use SQL commands to populate the tables with data.
### Populate Database with Initial Data
The database can be populated with initial data by first dumping the data into a fixture (fixtures can also be written manually).
1) To dump initial data from a specific database into a fixture (data.json for example), use the `dumpdata` command:
```bash
python manage.py dumpdata --exclude=auth.permission --exclude=contenttypes > ponder/fixtures/data.json
```
2) Fixtures can be JSON, XML, or YAML files. For YAML fixtures, `pip install PyYAML`.
3) To load to the database, run data migrations using the `loaddata` command:
```bash
python manage.py loaddata data.json
```
4) Then configure the group permissions from the Admin page.

### Local DB
The fixture can be used to load data to a local database. 
1) First connect to a local database, then configure the `DATABASES` dictionary in `settings.py` as follows:
```python
DATABASES = {
    'default': {
        'ENGINE': '<YOUR_BUILT_IN_DB_BACKEND>',
        'NAME': '<YOUR_LOCAL_DB_NAME>',
        'USER': '<YOUR_LOCAL_DB_USER>',
        'PASSWORD': '<YOUR_LOCAL_DB_USER_PASSWORD>',
        'HOST': 'localhost',
    }
}
```
2) Run migrations and use the command: `python manage.py loaddata data.json`
3) Note that running the loaddata command will reload the data from the fixture into the database, removing any changes that you might have made to the database tables.

### Testing
Use this command to run the tests in `tests.py`:
```bash
python manage.py test
```
Tests that require a database will run on a separate test database. Make sure that the `USER` in `settings.py` is granted privileges to create a database.
## Docker Image
- Docker Compose should be installed to build the app's container image. 
- On Windows or Mac systems, install Docker Desktop. It includes Docker Engine, Docker CLI client and Docker Compose.
- For information on how to install Docker Compose on Linux systems, the instructions are listed in this page: https://docs.docker.com/compose/install/
- The Docker directory currently includes only two files:
  - `Dockerfile`
  - `docker-compose.yml`	
- Include the following to the above directory:
  - `manage.py`
  - `mysite`
  - `ponder`
  - `requirements.txt`
- This should be the final Docker directory tree: 
```bash
.
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── __pycache__
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── ponder
    ├── __init__.py
    ├── __pycache__
    ├── admin.py
    ├── apps.py
    ├── fixtures
    ├── forms.py
    ├── migrations
    ├── test
    ├── models.py
    ├── static
    ├── tables.py
    ├── templates
    ├── urls.py
    └── views.py   
```
To build the Docker image:
- In the terminal, go to the top level directory and run the  command: `docker-compose up`
- This will build the image on Docker Desktop with multiple containers (web and db containers). Go to http://localhost:8000/ in your browser to view the running app. 
- You need to add localhost to `ALLOWED_HOSTS` in the `settings.py` file.
- To shutdown the services, type `CTRL-C` in the same shell or run `docker-compose down` from another shell.

## User Roles

The app has a complex relationship between different kinds of users. The roles are described in our [wiki](https://github.com/ponder-lab/Imperative-DL-Study-Web-App/wiki/Roles).
