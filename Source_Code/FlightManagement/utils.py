from datetime import datetime

from FlightManagement.models import User, Flight, Regulation
from FlightManagement import db
import hashlib

def get_user_by_id(user_id):
    return User.query.get(user_id)

def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def register(name, username, password):
    if name and username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        u = User(name=name, username=username.strip(), password=password)
        db.session.add(u)
        db.session.commit()

def load_flights():
    return Flight.query.all()

def get_flight_by_id(flight_id):
    return Flight.query.get(flight_id)

def check_flight(id, name, departing_at, arriving_at, plane, airline):
    if id and name and departing_at and arriving_at:
        flight = Flight.query.filter(Flight.id.__eq__(id.strip())).first()
        if flight:
            return "Mã chuyến bay đã tồn tại"
        else:
            departing_at = datetime.strptime(departing_at, "%Y-%m-%dT%H:%M")
            arriving_at = datetime.strptime(arriving_at, "%Y-%m-%dT%H:%M")
            duration = arriving_at - departing_at
            g1 = Regulation.query.filter(Regulation.name.__eq__("duration")).first()
            if g1:
                default_date = datetime(1900, 1, 1)
                g1 = g1.get_value()
                g1 = datetime.strptime(g1, "%H:%M:%S")
                if (duration.total_seconds() > (g1 - default_date).total_seconds()):
                    f = Flight(id=id, name=name,
                               departing_at=departing_at, arriving_at=arriving_at,
                               plane_id=plane, airline_id=airline)
                    db.session.add(f)
                    db.session.commit()
                    return "Lưu thành công"
                else:
                    return str(duration.total_seconds())
            else:
                return "Hiện không có quy định về thời gian bay tối thiểu"