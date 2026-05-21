# Parking Management App

Flask-based parking management app with admin and user portals. Admins can create parking lots, manage users, and monitor occupancy. Users can register, login, reserve and release parking spots. Built with SQLite, Flask-Login, Flask-SQLAlchemy for easy local deployment and rapid parking workflows.

## Features

- Admins can create parking lots, manage users, and view occupancy summaries.
- Users can register, login, reserve available spots, and release reservations.
- SQLite persistence keeps data locally in `parking.db`.

## Setup

1. Create a Python virtual environment:

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

4. Visit `http://127.0.0.1:5000` in your browser.

## Notes

- The app creates a default admin user `admin` automatically on first run.
- Admin login currently uses username only, so add password validation for production.
- Update `app.config['SECRET_KEY']` in `app.py` before deploying.
