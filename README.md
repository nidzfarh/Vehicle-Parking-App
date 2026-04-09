# Parking Management App

A simple Flask-based parking management system with separate admin and user interfaces.

## Features

- Admins can:
  - create parking lots
  - manage users
  - view summary of available and occupied parking spots
- Users can:
  - register and login
  - reserve an available parking spot
  - release a reserved spot

## Tech stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite

## Project structure

- `app.py` - application setup, Flask config, database initialization
- `routes.py` - route definitions for authentication, admin, and user functionality
- `models.py` - database models for users, admins, lots, spots, and reservations
- `database.py` - helper to create the default admin account
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates for pages and dashboards

## Setup

1. Create a Python virtual environment (recommended):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

4. Open the app in your browser:

```text
http://127.0.0.1:5000
```

## Default admin account

The app automatically creates an admin user with the username `admin` on first run.

> Note: In the current code, admin login is based only on the username and does not validate a password.

## User workflow

1. Register a new account using the register page.
2. Login with the registered credentials.
3. Reserve an available spot from the user dashboard.
4. Release the spot when finished.

## Admin workflow

1. Login with the username `admin`.
2. Create parking lots by providing a name, address, PIN code, price, and maximum number of spots.
3. Manage users from the admin users page.
4. View parking lot occupancy summary.

## Notes

- The app uses `sqlite:///parking.db` by default.
- The database file is created in the project root.
- If needed, update `app.config['SECRET_KEY']` and database settings in `app.py`.
