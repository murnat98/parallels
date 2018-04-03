# parallels

## Before start
* python3 -m venv env
* . env/bin/activate
* Create file settings.ini

### settings.ini structure
    [DEFAULT]
         SecretKey = secret_key
         debug = True or False

    [Database]
        name = db name
        user = user
        password = password
        host = host

## Start
* pip install -r requirements.txt
* ./manage.py migrate
* ./manage.py runserver <port>
