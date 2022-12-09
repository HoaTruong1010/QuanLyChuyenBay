from FlightManagement.models import User, Profile, AirPlane, Seat, AirPort, AirLine, Flight, Flight_AirportMedium, \
    PlaneTicket, Regulation
from FlightManagement import db
from flask_login import current_user
from sqlalchemy import func
import hashlib


def load_airports():
    return AirPort.query.all()


def load_airlines():
    return AirLine.query.all()


def load_tickets():
    return PlaneTicket.query.all()


def load_from_airlines(airport_id=None, kw=None):
    query = AirLine.query.filter()

    if airport_id:
        query = query.filter(AirLine.from_airport_id.__eq__(airport_id))

    if kw:
        query = query.filter(AirLine.name.contains(kw))

    return query.all()


def get_airport_by_id(airport_id):
    return AirPort.query.get(airport_id)


def get_airline_by_id(airline_id):
    return AirLine.query.get(airline_id)


def get_from_airport_by_id(from_airport_id):
    return AirLine.query.get(from_airport_id)


def get_to_airport_by_id(to_airport_id):
    return AirLine.query.get(to_airport_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)

# def save_receipt(cart):
#     if cart:
#         r = Receipt(user=current_user)
#         db.session.add(r)
#
#         for c in cart.values():
#             d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
#                                receipt=r, product_id=c['id'])
#             db.session.add(d)
#
#         db.session.commit()


# def count_product_by_cate():
#     return db.session.query(Category.id, Category.name, func.count(Product.id)) \
#         .join(Product, Product.category_id.__eq__(Category.id), isouter=True) \
#         .group_by(Category.id).order_by(Category.id).all()


# def stats_revenue(kw=None, from_date=None, to_date=None):
#     query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
#         .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)) \
#         .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))
#
#     if kw:
#         query = query.filter(Product.name.contains(kw))
#
#     if from_date:
#         query = query.filter(Receipt.created_date.__ge__(from_date))
#
#     if to_date:
#         query = query.filter(Receipt.created_date.__le__(to_date))
#
#     return query.group_by(Product.id).all()


# if __name__ == '__main__':
#     from FlightManagement import app
#
#     with app.app_context():
#         print(count_product_by_cate())
