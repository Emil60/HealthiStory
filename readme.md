Live on: `healthistory.herokuapp.com`

## About

The main app is HealtiStory, alongside this there are home(keeps static pages such as home page, contact page etc.),
account (for sign in and registration), product.
All HTML files are in templates folder. Css, images and js files are in static directory.
For multilingual web site all translations are in locale folder. 



### Instalation

Before running the server there is a need to configure database settings.

If you already installed mysqlclient just go to settings.py file and find DATABASES section and configure it, otherwise mysqlclient should be downloaded.

###### To do this open terminal and type:

(for windows) `pip install mysqlclient`
(for linux) `pip3 install mysqlclient`

###### In case command above does not work:
For Python 3.8: 
For linux OS you can also install the package in the project:

Run in terminal: `pip3 install mysqlclient-2.0.1-cp38-cp38-linux_x86_64.whl`

For Windows OS you can also install the package in the project:

 Run in terminal: `pip install mysqlclient-2.0.1-cp38-cp38-win_amd64.whl`

            
###### Next run: `pip install -r requirements.txt`

###### To run the server: `py manage.py runserver`

###### For unapplied migrations for Windows OS run in terminal:
`py manage.py makemigrations`

`py manage.py migrate`
    
###### For Linux OS:
`python3 manage.py makemigrations`

`python3 manage.py migrate`


###### To make new translations in terminal:
Run: `django-admin makemessages -l az`  (az is optional can be ru tr etc.)

The file with .po extension contains translatable stuff

Once the translations are run in terminal: `django-admin compilemessages`
