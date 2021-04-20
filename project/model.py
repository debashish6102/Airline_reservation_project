import datetime
from project import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M')
        return value


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    passenger = db.relationship('Passenger')
    booking_details = db.relationship('Booking_details')


class Flight(db.Model):
    flight_no = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    city_source = db.Column(db.String(10), nullable=False, )
    city_destination = db.Column(db.String(10), nullable=False)
    no_of_seats = db.Column(db.Integer, nullable=False)
    time_dept = db.Column(MyDateTime, nullable=False, )
    time_arrival = db.Column(MyDateTime, nullable=False, )
    time_duration = db.Column(db.Integer, nullable=False, )
    price = db.Column(db.Integer, nullable=False)


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airport_name = db.Column(db.String(50), unique=True, nullable=False)
    city_name = db.Column(db.String(30), nullable=False, unique=True)


class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Booking_details(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    flight_no = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
