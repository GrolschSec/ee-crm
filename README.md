---

# ee-crm

## Installation

### Setting up the Database

1. Install PostgreSQL:
    ```bash
    sudo apt install postgresql
    ```

2. Switch to the PostgreSQL user:
    ```bash
    sudo -i -u postgres
    ```

3. Create the database:
    ```sql
    CREATE DATABASE ee_db;
    ```

4. Create a user and set a password:
    ```sql
    CREATE USER epicevents WITH PASSWORD 'password';
    ```

5. Grant privileges to the user on the database:
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE ee_db TO epicevents;
    ```

6. Exit the PostgreSQL prompt:
    ```sql
    \q
    ```

### Configure Environment Variables

1. Add a `.env` file at the root of the repository with the following content:

    ```env
    DB_ENGINE=
    DB_HOST=
    DB_PORT=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=

    # JWT settings
    JWT_SECRET=
    JWT_ALGORITHM="HS256"
    JWT_TOKEN_LIFETIME="1"

    # Timezone settings
    TZ="Europe/Paris"

    # Phone settings
    PHONE_REGION="FR"

    # Sentry
    SENTRY_DSN=
    ```

2. Fill in the database variables with your database information.

3. Generate the JWT Secret using:
    ```bash
    openssl rand -base64 32
    ```

4. For Sentry, create an account at [Sentry](https://sentry.io/), create a project, and copy the Sentry DSN into the `.env` file.

### Apply Model Migrations to the Database

Once you have set the correct values in your `.env` file, follow these steps to apply model migrations:

1. Upgrade the database schema:
    ```bash
    alembic upgrade head
    ```

---

# Begin with the program 

at first there won't be any user in your database but so you need to be connected to an admin account or a account from the management team to create users in the crm.
Since the db is empty you can create a superuser with the following command:

python3 main.py user create --admin

E.g.: this command will only work if there is no admin in db (which should be the case).

You can now login with the new superuser and enjoy the crm add users ...

# Some about the permissions

If you get a permission denied during ...blabla explain the permissions

# Everything should work fine but you can test the code with the pytest included .....
