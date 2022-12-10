from FlightManagement.models import *
from FlightManagement import db

import hashlib
from datetime import datetime


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

def load_airports():
    return AirPort.query.all()


def take_time(str_date, format):
    default_date = datetime(1900, 1, 1)
    date = datetime.strptime(str_date, format)
    time = date - default_date
    return time


def get_regulation_time_by_id(id):
    date = Regulation.query.get(id)
    return take_time(date.get_value(), "%H:%M:%S")


def check_flight(id, name, departing_at, arriving_at, plane):
    if id and name and departing_at and arriving_at:
        flight = Flight.query.filter(Flight.id.__eq__(id.strip())).first()
        if flight:
            msg = "Mã chuyến bay đã tồn tại"
        else:
            departing_at = datetime.strptime(departing_at, "%Y-%m-%dT%H:%M")
            arriving_at = datetime.strptime(arriving_at, "%Y-%m-%dT%H:%M")
            duration = arriving_at - departing_at
            rt = get_regulation_time_by_id(5)
            if rt:
                if duration.total_seconds() > rt.total_seconds():
                    planes = Flight.query.filter(Flight.plane_id.__eq__(plane)).all()
                    if planes:
                        for p in planes:
                            if arriving_at < p.departing_at or p.arriving_at < departing_at:
                                msg = "success"
                            else:
                                msg = "Máy bay đã có lịch bay trong khoảng thời gian này"
                    else:
                        msg = "success"
                else:
                    msg = "Thời gian bay chưa đạt tối thiểu"
            else:
                msg = "Hiện không có quy định về thời gian bay tối thiểu"
        return msg

def save_flight(id, name, departing_at, arriving_at, plane, airline):
    al_id = AirLine.query.filter(AirLine.name.__eq__(airline)).first()
    f = Flight(id=id, name=name,
               departing_at=departing_at, arriving_at=arriving_at,
               plane_id=plane, airline_id=al_id.id)
    db.session.add(f)
    db.session.commit()


def check_airport_medium(name, min_stop, max_stop, airline, stop_airport, flight_id):
    if name and min_stop and max_stop:
        rt_min = get_regulation_time_by_id(6)
        rt_max = get_regulation_time_by_id(7)

        min_stop = datetime.strptime(min_stop, "%Y-%m-%dT%H:%M")
        max_stop = datetime.strptime(max_stop, "%Y-%m-%dT%H:%M")

        stop_duration = max_stop - min_stop
        if rt_min and rt_max:
            if stop_duration.total_seconds() >= rt_min.total_seconds() \
                    and stop_duration.total_seconds() <= rt_max.total_seconds():
                f = Flight.query.get(flight_id)
                if min_stop > f.departing_at and max_stop < f.arriving_at:
                    al = AirLine.query.filter(AirLine.name.__eq__(airline)).first()
                    ap = AirPort.query.filter(AirPort.name.__eq__(stop_airport)).first()
                    if ap.id != al.from_airport_id or ap.id !=al.to_airport_id:
                        apm = Flight_AirportMedium.query.filter(
                            Flight_AirportMedium.flight_id.__eq__(flight_id),
                            Flight_AirportMedium.airport_medium_id.__eq__(ap.id)
                        ).first()
                        if apm:
                            check_am_msg = 'Sân bay này đã được chọn làm trung gian. Vui lòng chọn sân bay khác!'
                        else:
                            check_am_msg = 'success'
                    else:
                        check_am_msg = 'Sân bay đã thuộc tuyến bay'
                else:
                    check_am_msg = 'Thời gian dừng không phù hợp với thời gian bay'
            else:
                check_am_msg = 'Thời gian dừng không đúng quy định'
        else:
            check_am_msg = 'Vui lòng thiết lập quy định về thời gian dừng tối thiểu và tối đa'
    else:
        check_am_msg = 'Thông tin chưa được điền đầy đủ'
    return check_am_msg

def save_airport_medium(name, min_stop, max_stop, description, flight_id, airport):
    ap = AirPort.query.filter(AirPort.name.__eq__(airport)).first()
    min_stop = datetime.strptime(min_stop, "%Y-%m-%dT%H:%M")
    max_stop = datetime.strptime(max_stop, "%Y-%m-%dT%H:%M")
    apm = Flight_AirportMedium(name=name, stop_time_begin=min_stop, stop_time_finish=max_stop,
               description=description, flight_id=flight_id, airport_medium_id=ap.id)
    db.session.add(apm)
    db.session.commit()