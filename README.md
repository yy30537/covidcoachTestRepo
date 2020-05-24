# Project Title

CS 361 Project Team03-COVIDCoach

## Setup:
Create a venv folder within the project folder:
```
$ python3 -m venv venv
```
To activate the environment:
```
$ . venv/bin/activate
```
Within the activated environment:
```
$ pip install Flask
$ pip install newsapi-python
$ pip install pandas
$ pip install flask-bootstrap
$ pip install flask-sqlalchemy
$ pip install flask-wtf
$ pip install email-validator
$ pip install flask-bcrypt
$ pip install flask-login
$ pip install PyJWT
$ pip install flask-mail
```
Start running the application:
```
$ export FLASK_APP=app.py
$ flask run
```

## if meet urllib error
Run
```
/Applications/Python\ 3.7/Install\ Certificates.command
```

## if app.db is existed before 4.28, delete it and open python console in pycharm
Run
```
from app.models import db
db.create_all()
```

## Authors

* **Meng Ding** 
* **Yiqiao Lu** 
* **Yang Yang** 
* **Zan Zhang** 
* **Yang Zhang** 
