## 1. Install Python packages
Open PowerShell in the project folder:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Install PostgreSQL
1. Download and install PostgreSQL from postgresql.org (keep port `5432`, remember the `postgres` password).
2. Create the database (in pgAdmin, or in a terminal):
```
psql -U postgres -c "CREATE DATABASE datheon;"
```

## 3. Create your `.env` file
Copy `.env.example` to `.env` and set:
- `DATABASE_URL` with your PostgreSQL password.
- The email settings
