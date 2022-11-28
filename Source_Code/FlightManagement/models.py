from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, DateTime, Enum, Time, Text
from sqlalchemy.orm import relationship
from FlightManagement import db, app, admin
from enum import Enum as UserEnum
from flask_login import UserMixin
import hashlib
from datetime import datetime
from flask_admin.contrib.sqla import  ModelView

class UserRole(UserEnum):
    USER = 1
    EMPLOYEE = 2
    ADMIN = 3


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())

    userRole = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.id


class Profile(db.Model):
    __tablename__ = 'profiles'

    serial = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(12), nullable=False)
    name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    dob = Column(DateTime, nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    isSupervisor = Column(Boolean, default=False)

    tickets = relationship('PlaneTicket', backref='profiles')

    def __str__(self):
        return self.serial


class AirPlane(db.Model):
    __tablename__ = 'airplanes'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    totalSeat = Column(Integer, nullable=False)

    seats = relationship('Seat', backref='airplanes')
    flights = relationship('Flight', backref='airplanes')

    def __str__(self):
        return self.id


class Seat(db.Model):
    __tablename__ = 'seats'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    status = Column(Boolean, default=False)

    plane_id = Column(String(10), ForeignKey(AirPlane.id), nullable=False)
    tickets = relationship('PlaneTicket', backref='seats')

    def __str__(self):
        return self.id


class AirPort(db.Model):
    __tablename__ = 'airports'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)

    flight_airports = relationship('Flight_AirportMedium', backref='airports')

    def __str__(self):
        return self.id


class AirLine(db.Model):
    __tablename__ = 'airlines'

    id = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)

    from_airport_id = Column(String(10), ForeignKey(AirPort.id),nullable=False)
    to_airport_id = Column(String(10), ForeignKey(AirPort.id), nullable=False)

    from_airport = relationship("AirPort", foreign_keys=[from_airport_id])
    to_airport = relationship("AirPort", foreign_keys=[to_airport_id])
    flights = relationship('Flight', backref='airlines')

    def __str__(self):
        return self.id


class Flight(db.Model):
    __tablename__ = 'flights'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    departing_at = Column(DateTime, nullable=False)
    arriving_at = Column(DateTime, nullable=False)

    plane_id = (Column(String(10), ForeignKey(AirPlane.id), nullable=False))
    airline_id = (Column(String(10), ForeignKey(AirLine.id), nullable=False))
    flight_airports = relationship('Flight_AirportMedium', backref='flights')
    tickets = relationship('PlaneTicket', backref='flights')

    def __str__(self):
        return self.id


class Flight_AirportMedium(db.Model):
    __tablename__ = 'flight_airport_mediums'

    id = Column(String(10), primary_key=True)
    stopTimeMin = Column(DateTime, nullable=False)
    stopTimeMax = Column(DateTime, nullable=False)
    description = Column(Text)

    flight_id = (Column(String(10), ForeignKey(Flight.id), nullable=False))
    airport_medium_id = (Column(String(10), ForeignKey(AirPort.id), nullable=False))

    def __str__(self):
        return self.id


class PlaneTicket(db.Model):
    __tablename__ = 'tickets'

    id = Column(String(10), primary_key=True)
    rank = Column(Integer, nullable=False)
    price = Column(DECIMAL(18,2), nullable=False)
    date = Column(DateTime, nullable=False)
    place = Column(String(100), nullable=False)

    profile_id = (Column(Integer, ForeignKey(Profile.serial), nullable=False))
    flight_id = (Column(String(10), ForeignKey(Flight.id), nullable=False))
    seat_id = (Column(String(10), ForeignKey(Seat.id), nullable=False))
    user_id = (Column(Integer, ForeignKey(User.id), nullable=False))

    def __str__(self):
        return self.id


# admin.add_view((ModelView()))

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        # db.create_all()

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u1 = User(name='An', username='an1100', password=password,
                 userRole=UserRole.USER)
        u2 = User(name='Binh', username='binh1211', password=password,
                  userRole=UserRole.EMPLOYEE)
        u3 = User(name='Dong', username='dong1100', password=password,
                  userRole=UserRole.ADMIN)
        db.session.add_all([u1, u2, u3])
        db.session.commit()
        #
        # p1 = Profile(id='01231', name='Nguyen Van An', gender='nam', dob=datetime(2002,1,1), email='an1100@gmail.com',
        #              phone='0176448394')
        # p2 = Profile(id='01232', name='Le Thi Binh', gender='nu', dob=datetime(2001, 11, 6), email='binh1211@gmail.com',
        #              phone='0176640394')
        # p3 = Profile(id='01233', name='Tran Van Dong', gender='nam', dob=datetime(2000, 4, 17), email='dong1100@gmail.com',
        #              phone='0176470094', isSupervisor=True)
        # db.session.add_all([p1, p2, p3])
        # db.session.commit()

        # pl1 = AirPlane(id='MB1', name='May bay 1', manufacturer='VN AirLine', totalSeat=60)
        # pl2 = AirPlane(id='MB2', name='May bay 2', manufacturer='VN AirLine', totalSeat=70)
        # pl3 = AirPlane(id='MB3', name='May bay 3', manufacturer='VN AirLine', totalSeat=65)
        # db.session.add_all([pl1, pl2, pl3])
        # db.session.commit()