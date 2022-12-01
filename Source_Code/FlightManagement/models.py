from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, DateTime, Enum, Time, Text
from sqlalchemy.orm import relationship
from FlightManagement import db, app, admin
from enum import Enum as UserEnum
from flask_login import UserMixin
import hashlib
from datetime import datetime, time
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
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    tickets = relationship('PlaneTicket', backref='users')

    def __str__(self):
        return str(self.id)


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
        return str(self.id)


class AirPlane(db.Model):
    __tablename__ = 'airplanes'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    totalSeat = Column(Integer, nullable=False)

    seats = relationship('Seat', backref='airplanes')
    flights = relationship('Flight', backref='airplanes')

    def __str__(self):
        return str(self.id)


class Seat(db.Model):
    __tablename__ = 'seats'

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    status = Column(Boolean, default=False)
    unit_price = Column(DECIMAL(18,2), nullable=False)

    plane_id = Column(String(10), ForeignKey(AirPlane.id), nullable=False)
    tickets = relationship('PlaneTicket', backref='seats')

    def __str__(self):
        return str(self.id)


class AirPort(db.Model):
    __tablename__ = 'airports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)

    flight_airports = relationship('Flight_AirportMedium', backref='airports')

    def __str__(self):
        return str(self.id)


class AirLine(db.Model):
    __tablename__ = 'airlines'

    id = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)

    from_airport_id = Column(Integer, ForeignKey(AirPort.id),nullable=False)
    to_airport_id = Column(Integer, ForeignKey(AirPort.id), nullable=False)

    from_airport = relationship("AirPort", foreign_keys=[from_airport_id])
    to_airport = relationship("AirPort", foreign_keys=[to_airport_id])
    flights = relationship('Flight', backref='airlines')

    def __str__(self):
        return str(self.id)


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
        return str(self.id)


class Flight_AirportMedium(db.Model):
    __tablename__ = 'flight_airport_mediums'

    id = Column(String(10), primary_key=True)
    stopTimeMin = Column(Time, nullable=False)
    stopTimeMax = Column(Time, nullable=False)
    description = Column(Text)

    flight_id = (Column(String(10), ForeignKey(Flight.id), nullable=False))
    airport_medium_id = (Column(Integer, ForeignKey(AirPort.id), nullable=False))

    def __str__(self):
        return str(self.id)


class PlaneTicket(db.Model):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(Integer, nullable=False)
    price = Column(DECIMAL(18,2), nullable=False)
    date = Column(DateTime, default=datetime.now())
    place = Column(String(100), nullable=False)

    profile_id = (Column(Integer, ForeignKey(Profile.serial), nullable=False))
    flight_id = (Column(String(10), ForeignKey(Flight.id), nullable=False))
    seat_id = (Column(String(10), ForeignKey(Seat.id), nullable=False))
    user_id = (Column(Integer, ForeignKey(User.id), nullable=False))

    def __str__(self):
        return str(self.id)


class Regulation(db.Model):
    __tablename__ = 'regulations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    value = Column(String(50), nullable=False)
    description = Column(Text)

    def __str__(self):
        return str(self.id)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Profile, db.session))
admin.add_view(ModelView(AirPlane, db.session))
admin.add_view(ModelView(Seat, db.session))
admin.add_view(ModelView(AirPort, db.session))
admin.add_view(ModelView(AirLine, db.session))
admin.add_view(ModelView(Flight, db.session))
admin.add_view(ModelView(Flight_AirportMedium, db.session))
admin.add_view(ModelView(PlaneTicket, db.session))
admin.add_view(ModelView(Regulation, db.session))


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        # db.create_all()

        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u1 = User(name='An', username='an1100', password=password,
        #          user_role=UserRole.USER)
        # u2 = User(name='Binh', username='binh1211', password=password,
        #           user_role=UserRole.EMPLOYEE)
        # u3 = User(name='Dong', username='dong1100', password=password,
        #           user_role=UserRole.ADMIN)
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()

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

        # s1 = Seat(id='G1', name='Ghế 1', plane_id='MB1')
        # s2 = Seat(id='G2', name='Ghế 2', plane_id='MB2')
        # s3 = Seat(id='G3', name='Ghế 3', plane_id='MB3')
        # db.session.add_all([s1, s2, s3])
        # db.session.commit()

        # sb1 = AirPort(name='Sân bay Nội Bài', location='Hà Nội')
        # sb2 = AirPort(name='Sân bay Tân Sơn Nhất', location='Hồ Chí Minh')
        # sb3 = AirPort(name='Sân bay Phù Cát', location='Bình Định')
        # db.session.add_all([sb1, sb2, sb3])
        # db.session.commit()

        # al1 = AirLine(id='1', name='Hà Nội - Hồ Chí Minh', from_airport_id='1', to_airport_id='2')
        # al2 = AirLine(id='2', name='Hà Nội - Bình Định', from_airport_id='1', to_airport_id='3')
        # al3 = AirLine(id='3', name='Bình Định - Hồ Chí Minh', from_airport_id='3', to_airport_id='2')
        # db.session.add_all([al1, al2, al3])
        # db.session.commit()

        # f1 = Flight(id='CB1', name='Chuyến bay 001', departing_at=datetime(2022, 12, 1, 13, 00, 00),
        #             arriving_at=datetime(2022, 12, 1, 14, 00, 00), plane_id='MB1', airline_id='1')
        # f2 = Flight(id='CB2', name='Chuyến bay 002', departing_at=datetime(2022, 12, 1, 18, 00, 00),
        #             arriving_at=datetime(2022, 12, 1, 19, 00, 00), plane_id='MB2', airline_id='2')
        # f3 = Flight(id='CB3', name='Chuyến bay 003', departing_at=datetime(2022, 12, 1, 9, 00, 00),
        #             arriving_at=datetime(2022, 12, 1, 9, 50, 00), plane_id='MB3', airline_id='3')
        # db.session.add_all([f1, f2, f3])
        # db.session.commit()

        # fam1 = Flight_AirportMedium(id='TG1', stopTimeMin=time(0, 20, 00), stopTimeMax=time(0, 20, 00),
        #                             description="CB được nghỉ tại đây 20 phút", flight_id='CB1',
        #                             airport_medium_id='3')
        # db.session.add(fam1)
        # db.session.commit()

        # t1 = PlaneTicket(rank='2', price=1800000, place="Sân bay Nội bài", profile_id='1',
        #                  flight_id='CB1', seat_id='G1', user_id='2')
        # t2 = PlaneTicket(rank='1', price=2000000, place="Sân bay Nội bài", profile_id='2',
        #                  flight_id='CB2', seat_id='G1', user_id='2')
        # t3 = PlaneTicket(rank='1', price=1400000, place="Sân bay Phù Cát", profile_id='3',
        #                  flight_id='CB3', seat_id='G2', user_id='2')
        # db.session.add_all([t1, t2, t3])
        # db.session.commit()

        g1 = Regulation(name='book_time', value='12:00:00',
                        description='Thời gian đặt vé trước 12h lúc chuyến bay khởi hành')
        g2 = Regulation(name='sale_time', value='4:00:00',
                        description='Thời gian bán vé trước 4h lúc chuyến bay khởi hành')
        g3 = Regulation(name='rank_1', value='300000',
                        description='Vé hạng 1 phụ thu 300.000 VND')
        db.session.add_all([g1, g2, g3])
        db.session.commit()
        pass