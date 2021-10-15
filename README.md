# Imperative-DL-Study-Web-App
![Django CI](https://github.com/ponder-lab/Imperative-DL-Study-Web-App/actions/workflows/django.yml/badge.svg)

Web App for the Imperative DL Study
https://fathomless-inlet-57767.herokuapp.com

## Setup/Run Instructions
### Pre-requisites
- Ensure Django is set up: https://docs.djangoproject.com/en/3.1/topics/install/
- Ensure mysql is set up: https://dev.mysql.com/doc/refman/8.0/en/installing.html
    - Additionally, also ensure `mysqlclient` is installed (either via Brew or other methods) https://pypi.org/project/mysqlclient/
- Ensure the below PATH is exported in your environment `export DYLD_LIBRARY_PATH="/usr/local/mysql/lib/"`

### Run Instructions
1) Ensure all pre-requisites above are met.
2) Install dependencies: `pip install -r requirements.txt`
3) Run the app: `python manage.py runserver`
4) Navigate to: `localhost:8000` to view the app.
5) If you need an account, use the below admin account credentials to create one for our Heroku db.

- Debug: If the above `localhost:8000` page throws an access error, consider adding `localhost` to `ALLOWED_HOSTS` in the `settings.py` file.
- Debug: If you run into error regarding `STATIC_ROOT` see: https://github.com/OpenToAllCTF/OTA-University/issues/9 suggestion to change `STATIC_ROOT` assignment to just `/static/`

### Docker
- Docker Compose should be installed to build the app's container image. 
- On Windows or Mac systems, install Docker Desktop. It includes Docker Engine, Docker CLI client and Docker Compose.
- For information on how to install Docker Compose on Linux systems, the instructions are listed in this page: https://docs.docker.com/compose/install/
- The Docker directory currently includes only two files:
  - Dockerfile
  - docker-compose.yml	

- Include the following to the above directory:
  - manage.py
  - mysite
  - ponder
  - requirements.txt

- This should be the final Docker directory tree: 
```bash
    .
    ├── Dockerfile
    ├── docker-compose.yml
    ├── manage.py
    ├── mysite
    │   ├── __pycache__
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── ponder
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── filters.py
    │   ├── forms.py
    │   ├── migrations
    │   ├── models.py
    │   ├── static
    │   ├── tables.py
    │   ├── templates
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    └── requirements.txt
    
```

To build the Docker image:

- In the terminal, go to the top level directory and run the  command: `docker-compose up`
- This will build the image on Docker Desktop with multiple containers (web and db containers). Go to http://localhost:8000/ in your browser to view the running app. 
- You need to add localhost to ALLOWED HOSTS in the settings.py file.
- To shutdown the services, type `CTRL-C` in the same shell or run `docker-compose down` from another shell.

### Local DB
The app by default connects to our Heroku DB using the settings provided in `settings.py`. Run the below command to get a mysql dump of our latest DB from Heroku.

1) Run the following commands to import a base MySQL dump of the heroku database to your local db: `mysql -u <USERNAME> -p <DATA_BASE_NAME> < sql_dump_file.sql`
2) Then, in our `settings.py` update our `DATABASE` config value using the below example:
```python
DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<YOUR_LOCAL_DB_NAME>',
        'USER': '<YOUR_LOCAL_DB_USER>',
        'PASSWORD': '<YOUR_LOCAL_DB_USER_PASSWORD>',
        'HOST': 'localhost',
        'OPTIONS': {'ssl_mode': 'DISABLED'}
    }
}
```
3) Finally, we can run the migrate command to have Django update our imported DB with any future updates/changes that were done to our db from our migrate file: 
```bash
python manage.py migrate
```

To get an up to date schema of our DB from Heroku, we can also connect directly to it to fetch a MySQL dump of the DB by running the command below:
```bash
mysqldump --no-tablespaces --column-statistics=0 --host=us-cdbr-east-03.cleardb.com --user=be05ffb901b132 --password=3d94000c heroku_4ac11fb2946b4e7 > sql_dump_file.sql
```

The host, password and username that we used above to connect to our Heroku DB can all be found in our `settings.py` in case it changes in the future.

### Test Database
1) In `mysite/test_settings.py`, configure the `DATABASE` dictionary values to connect to your local database.
2) Use this command to run the tests:
```bash
python manage.py test ponder --settings=mysite.test_settings
```

## Admin Account

Field | Value
-- | --
Username | admin
Password | umjawaRZ7GY5C7Q

You can use this to register for accounts in the web app that is deployed on Heroku.
