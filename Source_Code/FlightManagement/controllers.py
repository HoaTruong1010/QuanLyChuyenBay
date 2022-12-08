from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user

from FlightManagement import utils
from FlightManagement.models import *


def index():
    return render_template("index.html")


def login_my_user():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            if user.user_role == UserRole.ADMIN:
                return redirect('/admin')

            return redirect(url_for("index"))
        else:
            err_msg = "ĐĂNG NHẬP THẤT BẠI!!!"

    return render_template("index.html", err_msg=err_msg)


def logout_my_user():
    logout_user()
    return redirect(url_for("index"))


def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            try:
                utils.register(name=request.form['name'],
                             password=password,
                             username=request.form['username'])

                return redirect('/')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


def airports():
    data = []

    for a in utils.load_airports():
        data.append({
            'id': a.id,
            'name': a.name
        })

    return jsonify(data)

