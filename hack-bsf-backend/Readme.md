# INSTALL COMMANDS

- Go to Project Root Folder.
```bash
python3 -m venv venv-bsf
source venv-bsf/bin/activate
pip install -r requirements.txt
```
- If the DB details are available first setup the details in bsf/settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'BigSolutionFinder',
        'USER': 'dbuser',
        'PASSWORD': 'secret-sql-pw',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

# FIRST TIME DB SETUP
From Root folder of the project. 
If the DB is new.
```bash
python manage.py makemigrations
python manage.py migrate
```
# PROJECT INITIATION COMMANDS
Commands to start new project and app.
```bash
django-admin startproject bsf .
python manage.py startapp bsfbackend
```

# Setting up mysql Docker for Django Part.
Docker commands to work with local mysql DB
```bash
docker pull mysql
docker run --name=mysql-container -e MYSQL_ROOT_PASSWORD=secret-sql-pw -d -p 3306:3306 mysql
```