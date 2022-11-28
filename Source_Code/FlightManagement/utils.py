from FlightManagement.models import User
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