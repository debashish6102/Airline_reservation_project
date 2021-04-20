from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .model import Flight, Airport, Passenger, Booking_details

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home', methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        airport_from = request.form.get('airport_from')
        airport_to = request.form.get('airport_to')
        seats = request.form.get('seats')
        date = request.form.get('date')
        flight = Flight.query.filter_by(city_source=airport_from, city_destination=airport_to).all()
        return render_template("flight_detail.html", flight=flight, user=current_user)
    return render_template("index.html", user=current_user)


@views.route('/passenger_detail/<int:flight_no>', methods=['GET', 'POST'])
def passenger_detail_page(flight_no):
    new_booking = Booking_details(flight_no=flight_no, user_id=current_user.id)
    db.session.add(new_booking)
    db.session.commit()
    if request.method == "POST":
        passenger_name = request.form.get('passenger_name')
        passenger_age = request.form.get('passenger_age')
        passenger_sex = request.form.get('passenger_sex')
        passenger = Passenger.query.filter_by(name=passenger_name).first()
        if passenger:
            flash('this passenger is already in your record', category='error')
            passenger = Passenger.query.filter_by(user_id=current_user.id).all()
            return render_template("passenger_detail.html", user=current_user, passenger=passenger)
        else:
            new_passenger = Passenger(name=passenger_name, age=passenger_age, gender=passenger_sex,
                                      user_id=current_user.id)
            db.session.add(new_passenger)
            db.session.commit()
            passenger = Passenger.query.filter_by(user_id=current_user.id).all()
            flash('passenger added', category='success')
            return render_template("passenger_detail.html", user=current_user, passenger=passenger)
    return render_template("passenger_detail.html", user=current_user)


@views.route('/add_flights', methods=['GET', 'POST'])
def add_flights():
    if request.method == "POST":
        flight_num = request.form.get('flight_num')
        city_source = request.form.get('city_source')
        city_dest = request.form.get('city_dest')
        num_seats = request.form.get('num_seats')
        time_dept = request.form.get('time_dept')
        time_arrival = request.form.get('time_arrival')
        time_duration = request.form.get('time_duration')
        price = request.form.get('price')
        flight = Flight.query.filter_by(flight_no=flight_num).first()
        if flight:
            flash('error This number is already present', category='error')
        elif city_dest == city_source:
            flash('error source and destination can not be same', category='error')
        elif num_seats == 0:
            flash('error seats can not be zero', category='error')
        elif price == 0:
            flash('error price can not be zero', category='error')
        else:
            new_flight = Flight(flight_no=flight_num, city_source=city_source, city_destination=city_dest,
                                no_of_seats=num_seats,
                                time_dept=time_dept, time_arrival=time_arrival, time_duration=time_duration,
                                price=price)
            db.session.add(new_flight)
            db.session.commit()
            flash('flight added!', category='success')
            return redirect(url_for('views.add_flights'))
    return render_template("admin_flight.html", user=current_user)


@views.route('/contact_us')
def contact_us_page():
    return render_template('contact_us.html', user=current_user)


@views.route('/about_us')
def about_us_page():
    return render_template('about_us.html', user=current_user)


@views.route('/flight_detail', methods=['GET', 'POST'])
def flight_detail_page():
    return render_template('flight_detail.html', user=current_user)


@views.route('/my_trips', methods=['GET', 'POST'])
def my_trips_page():
    booking = Booking_details.query.filter_by(user_id=current_user.id).all()
    flights = Flight.query.filter_by(flight_no=Booking_details.flight_no)
    return render_template('mytrip.html', user=current_user, booking=booking, flights=flights)


@views.route('/add_airports', methods=['GET', 'POST'])
def add_airports_page():
    if request.method == "POST":
        port_name = request.form.get('port_name')
        city_name = request.form.get('city_name')
        airport = Airport.query.filter_by(airport_name=port_name).first()
        if airport:
            flash('error This name is already present', category='error')
        else:
            new_airport = Airport(city_name=city_name, airport_name=port_name)
            db.session.add(new_airport)
            db.session.commit()
            flash('airport added!', category='success')
            return redirect(url_for('views.add_airports_page'))
    return render_template('admin_airport.html', user=current_user)


@views.route('/payment', methods=['GET', 'POST'])
def payment_page():
    return render_template('payment.html', user=current_user)


@views.route('/delete/<int:id>')
def delete(id):
    del_trip = Booking_details.query.get_or_404(id)
    db.session.delete(del_trip)
    db.session.commit()
    return redirect(url_for('views.my_trips_page'))

