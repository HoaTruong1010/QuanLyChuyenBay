from flask import render_template, request, redirect, session, jsonify
from FlightManagement import app, dao, utils
from flask_login import login_user, logout_user, login_required
from FlightManagement.decorators import anonymous_user
import cloudinary.uploader


def index():
    airports = dao.load_airports()
    from_airports = dao.load_from_airlines(airport_id=request.args.get("airport_id"),
                                           kw=request.args.get('keyword'))
    to_airports = dao.load_to_airlines(airport_id=request.args.get("airport_id"),
                                           kw=request.args.get("keyword"))
    tickets = dao.load_tickets()
    return render_template('index.html', airports=airports, from_airports=from_airports, to_airports=to_airports,
                           tickets=tickets)


def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


def booking():
    airports = dao.load_airports()
    return render_template('booking.html', airports=airports)


def booking_staff():
    from_airports = dao.load_from_airlines(airport_id=request.args.get("airport_id"),
                                           kw=request.args.get('keyword'))
    return render_template('booking_staff.html', from_airports=from_airports)


def from_airport(from_airport_id):
    f = dao.get_from_airport_by_id(from_airport_id)
    return render_template('index.html', airline=f)

# def booking_ticket(airline_id):
#     a = dao.get_airline_by_id(airline_id)
#     return render_template('details.html', airline=a)


# @login_required
# def pay():
#     key = app.config['CART_KEY']
#     cart = session.get(key)
#
#     try:
#         dao.save_receipt(cart)
#     except:
#         return jsonify({'status': 500})
#     else:
#         return jsonify({'status': 200})


# def cart():
#     # session['cart'] = {
#     #     "1": {
#     #         "id": "1",
#     #         "name": "iPhone 13",
#     #         "price": 12000,
#     #         "quantity": 2
#     #     },
#     #     "2": {
#     #         "id": "2",
#     #         "name": "iPhone 14",
#     #         "price": 15000,
#     #         "quantity": 1
#     #     }
#     # }
#
#     return render_template('cart.html')


# def add_to_cart():
#     data = request.json
#
#     id = str(data['id'])
#     name = data['name']
#     price = data['price']
#
#     key = app.config['CART_KEY']
#     cart = session.get(key, {})
#
#     if id in cart:
#         cart[id]['quantity'] += 1
#     else:
#         cart[id] = {
#             "id": id,
#             "name": name,
#             "price": price,
#             "quantity": 1
#         }
#
#     session[key] = cart
#
#     return jsonify(utils.cart_stats(cart))


# def update_cart(product_id):
#     key = app.config['CART_KEY']
#     cart = session.get(key)
#     if cart and product_id in cart:
#         quantity = int(request.json['quantity'])
#         cart[product_id]['quantity'] = quantity
#
#     session[key] = cart
#
#     return jsonify(utils.cart_stats(cart))


# def delete_cart(product_id):
#     key = app.config['CART_KEY']
#     cart = session.get(key)
#     if cart and product_id in cart:
#         del cart[product_id]
#
#     session[key] = cart
#
#     return jsonify(utils.cart_stats(cart))
