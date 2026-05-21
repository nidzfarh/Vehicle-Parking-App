from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db, User, Admin
from database import create_admin
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ko-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = Admin.query.get(int(user_id))
    if user:
        return user
    return User.query.get(int(user_id))

from routes import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)

    #app.run(host='0.0.0.0', port=5000, debug=True)
@app.route('/admin/delete_lot/<int:lot_id>', methods=['POST'])
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    if any(spot.status == 'O' for spot in lot.spots):
        flash("Cannot delete lot: Some spots are still occupied.", "danger")
        return redirect(url_for('admin_dashboard'))

    for spot in lot.spots:
        db.session.delete(spot)

    db.session.delete(lot)
    db.session.commit()

    flash("Parking lot deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))
