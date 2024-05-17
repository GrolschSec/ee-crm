Here's an improved version of the second part of your README, with better formatting, added explanations, and a more structured flow:

---

# ee-crm

## Installation

### Cloning the Repository

1. Clone the repository:
    ```bash
    git clone https://github.com/GrolschSec/ee-crm.git
    ```
2. Move into the repository directory:
    ```bash
    cd ee-crm/
    ```

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

### Install Python Dependencies

1. Create a virtual environment:
    ```bash
    python3 -m venv env
    ```

2. Activate the virtual environment:
    - On MacOS/Linux:
        ```bash
        source env/bin/activate
        ```
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```

3. Install the program dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

### Apply Model Migrations to the Database

Once you have set the correct values in your `.env` file, follow these steps to apply model migrations:

1. Upgrade the database schema:
    ```bash
    alembic upgrade head
    ```

---

## Starting the Program

Initially, there won't be any users in your database. You need to be connected to an admin account or an account from the management team to create users in the CRM. Since the database is empty, you can create a superuser with the following command:

```bash
python3 main.py user create --admin
```

**Note:** This command will only work if there is no admin in the database, which should be the case initially.

You can now log in with the new superuser and start using the CRM to add users and manage other functionalities.

You can see the list of the commands using:
```bash
python3 main.py --help
```
---
