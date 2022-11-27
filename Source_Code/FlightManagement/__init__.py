from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.secret_key='rtytr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:10102002@localhost/flight_management_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="QUAN LY CHUYEN BAY", template_mode="bootstrap5")