# ee-crm

## Generate JWT Secret

openssl rand -base64 32


# Setup the db

apt install postgresql

sudo -i -u postgres

CREATE DATABASE ee_db;

CREATE USER epicevents WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE ee_db TO epicevents;

\q

# Migrate the database using alembic

Once you'll have setted the good value in your .env file you can follow these steps

alembic upgrade head


# Begin with the program 

at first there won't be any user in your database but so you need to be connected to an admin account or a account from the management team to create users in the crm.
Since the db is empty you can create a superuser with the following command:

python3 main.py user create --admin

E.g.: this command will only work if there is no admin in db (which should be the case).

You can now login with the new superuser and enjoy the crm add users ...

# Some about the permissions

If you get a permission denied during ...blabla explain the permissions

# Everything should work fine but you can test the code with the pytest included .....