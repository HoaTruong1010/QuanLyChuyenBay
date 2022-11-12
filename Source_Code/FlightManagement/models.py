from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, DateTime, Enum, Time, Text
from sqlalchemy.orm import relationship
from FlightManagement import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin

class UserRole(UserEnum):
    USER = 1
    EMPLOYEE = 2
    ADMIN = 3


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    avatar = Column(String(100), nullable=False)
    join_date = Column(DateTime, nullable=False)

    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.id


class Profile(db.Model):
    __abstract__ = True

    serial = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(12), nullable=False)
    name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    dob = Column(DateTime, nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)


class Customer(Profile):
    __tablename__ = 'customers'

    plane_tickets = relationship('PlaneTicket', backref='customers')

    def __str__(self):
        return self.name


class Employee(Profile):
    __tablename__ = 'employees'

    is_Supervisor = Column(Boolean, default=False)

    tickets = relationship('PlaneTicket', backref='employees')

    def __str__(self):
        return self.name


class AirPlane(db.Model):
    __tablename__ = 'airplanes'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    totalSeat = Column(Integer, nullable=False)
    numberOfFistClassSeat = Column(Integer, nullable=False)
    numberOfAvailableFistClassSeat = Column(Integer, nullable=False)

    seats = relationship('Seat', backref='airplane')
    flights = relationship('Flight', backref='airplane')

    def __str__(self):
        return self.name


class Seat(db.Model):
    __tablename__ = 'seats'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    status = Column(Boolean, nullable=False)

    plane_id = Column(String(10), ForeignKey(AirPlane.id), nullable=False)
    tickets = relationship('PlaneTicket', backref='seat')

    def __str__(self):
        return self.name


class AirPort(db.Model):
    __tablename__ = 'airports'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)

    airlines = relationship('AirLine', backref='airport')
    flight_airports = relationship('Flight_AirportMedium', backref='airport')

    def __str__(self):
        return self.name


class AirLine(db.Model):
    __tablename__ = 'airlines'

    id = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)

    from_airport = Column(String(10), ForeignKey(AirPort.id),nullable=False)
    to_airport = Column(String(10), ForeignKey(AirPort.id), nullable=False)
    flights = relationship('Flight', backref='airline')

    def __str__(self):
        return self.name


class Flight(db.Model):
    __tablename__ = 'flights'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    departing_at = Column(DateTime, nullable=False)
    arriving_at = Column(DateTime, nullable=False)

    plane_id = (Column(String(10), ForeignKey(AirPlane.id), nullable=False))
    airline_id = (Column(String(10), ForeignKey(AirLine.id), nullable=False))
    flight_airports = relationship('Flight_AirportMedium', backref='flight')
    tickets = relationship('PlaneTicket', backref='flight')

    def __str__(self):
        return self.name


class Flight_AirportMedium(db.Model):
    __tablename__ = 'flight_airport_mediums'

    id = Column(String(10), primary_key=True)
    stop_time = Column(DateTime, nullable=False)
    continue_time = Column(DateTime, nullable=False)
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

    customer_id = (Column(Integer, ForeignKey(Customer.serial), nullable=False))
    flight_id = (Column(String(10), ForeignKey(Flight.id), nullable=False))
    seat_id = (Column(String(10), ForeignKey(Seat.id), nullable=False))
    user_id = (Column(String(10), ForeignKey(User.id), nullable=False))
    employee_id = (Column(Integer, ForeignKey(Employee.serial), nullable=False))

    def __str__(self):
        return self.id


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

