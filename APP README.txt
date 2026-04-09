Vehicle Parking App - README

AUTHOR: NIDA FARHEEN C M
ROLL NO: 24F1001163

This is a web-based Vehicle Parking Management System developed using Flask, SQLite, HTML/CSS/Bootstrap, and Jinja2.

The app is role based. Two roles: admin and user

Features:
•	Admin login and dashboard
•	Admin can add parking lots and spots
•	Admin can delete a parking lot only if all spots are empty.
•	Admin can view available/occupied spots with charts showing parking summary.
•	Spot availability updated in real-time
•	Users can view available spots and reserve them
•	Responsive and interactive
•	Basic session-based login and access control

Project Structure
project/
│
├── app.py                 
├── models.py              
├── database.py            
├── routes.py              
├── templates/         
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── admin_summary.html etc
├── instance/
│   └── parking.db        
├── requirements.txt       
└── README.txt            

Setup Instructions
1. Install Dependencies
   Ensure you have Python 3 installed.
2. Initialize the Database
In app.py, database is auto-created using:
python
with app.app_context():
    db.create_all()
    create_admin()
3. Run the app python app.py
4. Open: http://127.0.0.1:5000/

