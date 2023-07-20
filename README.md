**HIGH5 BACKEND SETUP INSTRUCTIONS**

To run the project without docker follow these instructions

 - `git clone <repo-url>`
 - `cd High5-Cloud`
 - `python3 -m venv venv`
 - `source venv/bin/activate`
 - `cd core`
 - Change the environment variables in `env.txt` file and rename it to `.env`
 - `pip install -r requirements.txt`
 -  If you get some errors for the psycopg2 library, you need to install libpq-dev and gcc in your system.
 - `./manage.py makemigrations`
 - `./manage.py migrate`
 - `./manage.py createsuperuser`
 - `./manage.py runserver`
 
 To run the project using docker (Make sure docker is installed in your system)
 - `git clone <repo-url>`
 - `cd High5-Cloud`
 - `cd core`
 - Change the environment variables in `env.txt` file and rename it to `.env`
 -  `docker-compose up --build` or to run docker in detached mode `docker-compose up --build -d`
 - You can use management command like this `docker-compose exec backend python3 manage.py makemigrations` , `docker-compose exec backend python3 manage.py migrate`, ... etc