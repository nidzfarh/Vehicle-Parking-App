from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Admin, ParkingLot, ParkingSpot
from app import app

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exists!")
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. You can now login.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            login_user(admin)
            return redirect(url_for('admin_dashboard'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('user_dashboard'))

        flash("Invalid credentials.")
    return render_template("login.html")


from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import db, Admin, ParkingLot, ParkingSpot
from app import app

@app.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not isinstance(current_user._get_current_object(), Admin):
        flash("Access denied.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        pin = request.form['pin']
        price = float(request.form['price'])
        max_spots = int(request.form['max_spots'])

        # Create new parking lot
        new_lot = ParkingLot(
            prime_location_name=name,
            address=address,
            pin_code=pin,
            price=price,
            max_spots=max_spots
        )
        db.session.add(new_lot)
        db.session.commit()

        # Auto-create parking spots
        for _ in range(max_spots):
            spot = ParkingSpot(
                lot_id=new_lot.id,
                status='A'
            )
            db.session.add(spot)

        db.session.commit()
        flash("New parking lot created!")

    lots = ParkingLot.query.all()
    return render_template('admin_dashboard.html', lots=lots)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

from datetime import datetime
from models import Reservation, ParkingSpot

@app.route('/user/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    if isinstance(current_user._get_current_object(), Admin):
        flash("Admins cannot access user dashboard.")
        return redirect(url_for('admin_dashboard'))

    lots = ParkingLot.query.all()
    current_reservation = Reservation.query.filter_by(user_id=current_user.id, end_time=None).first()

    if request.method == 'POST':
        selected_lot_id = int(request.form['lot_id'])

        if current_reservation:
            flash("You already have a spot reserved.")
            return redirect(url_for('user_dashboard'))

        spot = ParkingSpot.query.filter_by(lot_id=selected_lot_id, status='A').first()
        if not spot:
            flash("No available spots in this lot.")
            return redirect(url_for('user_dashboard'))

        spot.status = 'O'
        reservation = Reservation(
            spot_id=spot.id,
            user_id=current_user.id,
            start_time=datetime.now(),
            cost_per_hour=ParkingLot.query.get(selected_lot_id).price
        )
        db.session.add(reservation)
        db.session.commit()
        flash(f"Spot {spot.id} reserved successfully!")

        return redirect(url_for('user_dashboard'))

    return render_template('user_dashboard.html', lots=lots, reservation=current_reservation)
@app.route('/release_spot')
@login_required
def release_spot():
    reservation = Reservation.query.filter_by(user_id=current_user.id, end_time=None).first()
    if reservation:
        reservation.end_time = datetime.now()
        reservation.spot.status = 'A'
        db.session.commit()
        flash("Spot released successfully.")
    else:
        flash("No active reservation found.")
    return redirect(url_for('user_dashboard'))
from models import User
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Admin

@app.route('/admin/users')
@login_required
def manage_users():
    if not isinstance(current_user._get_current_object(), Admin):
        flash("Access denied.")
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not isinstance(current_user._get_current_object(), Admin):
        flash("Access denied.")
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)

    if user.username == 'admin':
        flash("Admin account cannot be deleted.")
        return redirect(url_for('manage_users'))

    db.session.delete(user)
    db.session.commit()
    flash(f"User '{user.username}' deleted.")
    return redirect(url_for('manage_users'))

from flask import render_template
from models import ParkingLot, ParkingSpot
@app.route("/admin/summary")
def admin_summary():
    lots = ParkingLot.query.all()

    lot_names = []
    total_spots = []
    available_spots = []
    occupied_spots = []

    for lot in lots:
        spots = lot.spots
        total = len(spots)
        available = sum(1 for spot in spots if spot.status == 'A')  # A = Available
        occupied = total - available

        lot_names.append(lot.prime_location_name)
        total_spots.append(total)
        available_spots.append(available)
        occupied_spots.append(occupied)

    return render_template(
        "admin_summary.html",
        lot_names=lot_names,
        total_spots=total_spots,
        available_spots=available_spots,
        occupied_spots=occupied_spots
    )

