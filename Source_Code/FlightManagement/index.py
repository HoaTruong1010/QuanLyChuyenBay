from flask import render_template, request, redirect, url_for
from FlightManagement import app, login, utils, controllers
from FlightManagement.models import *
from flask_login import login_user, logout_user

app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/booking', 'booking', controllers.booking)


@app.route("/", methods=['get', 'post'])
def login_my_user():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for("index"))
        else:
            err_msg = "ĐĂNG NHẬP THẤT BẠI!!!"

    return render_template("index.html", err_msg=err_msg)


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect(url_for("index"))


@app.route('/register', methods=['get', 'post'])
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


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
