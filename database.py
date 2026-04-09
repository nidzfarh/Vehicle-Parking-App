from models import db, Admin

def create_admin():
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin')
        db.session.add(admin)
        db.session.commit()
