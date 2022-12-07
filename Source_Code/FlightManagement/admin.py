from flask import redirect, url_for, request
from flask_admin import Admin, expose, BaseView
from flask_login import current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import SelectField

from FlightManagement import utils

from FlightManagement import app, db
from FlightManagement.models import *
from flask_admin.contrib.sqla import ModelView

admin = Admin(app=app, name="AFFORDA", template_mode="bootstrap4")


class Base_View(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    # edit_modal = True
    # details_modal = True
    page_size = 10


class AuthenticatedModelView(Base_View):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class RegulationView(AuthenticatedModelView):
    column_filters = ['name', 'description']
    column_searchable_list = ['name', 'description']
    column_labels = {
        'id': 'ID',
        'name': 'Tên quy định',
        'value': 'Giá trị',
        'description': 'Mô tả'
    }


class Form(FlaskForm):
    airports = SelectField('airports', choices=[])
    airports2 = SelectField('airports2', choices=[])
    planes = SelectField('planes', choices=[])
    airlines = SelectField('airlines', choices=[])


class FlightManagementView(AuthenticatedModelView):
    column_filters = ['name', 'id']
    column_searchable_list = ['name', 'id']
    column_exclude_list = ['planes', 'airlines']
    column_labels = {
        'id': 'Mã chuyến bay',
        'name': 'Tên chuyến bay',
        'departing_at': 'Thời gian khởi hành',
        'arriving_at': 'Thời gian đến',
        'planes': 'Số hiệu máy bay',
        'airlines': 'Tuyến bay'
    }

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        sts_msg = ''
        am_msg1 = ''
        am_msg2 = ''
        form = Form()
        form.planes.choices = [p.id for p in AirPlane.query.all()]
        form.airlines.choices = [a.name for a in AirLine.query.all()]
        form.airports.choices = [ap.name for ap in AirPort.query.all()]

        if request.method == "POST":
            id = request.form['id']
            name = request.form['name']
            departing_at = request.form['departing_at']
            arriving_at = request.form['arriving_at']
            plane = form.planes.data
            airline = form.airlines.data

            sts_msg = utils.check_flight(id, name, departing_at, arriving_at, plane)
            if sts_msg == 'success':
                try:
                    utils.add_flight(id, name,departing_at, arriving_at, plane, airline)
                except:
                    sts_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'

            try:
                is_apm = request.form['isMedium']
                if is_apm == 'on':
                    am_number = request.form['number']

                    if am_number == '1' or am_number == '2':
                        am_name1 = request.form['name-stop']
                        am_min_stop1 = request.form['time-stop-min']
                        am_max_stop1 = request.form['time-stop-max']
                        am_description1 = request.form['description']
                        am_airport1 = form.airports.data
                        am_msg1 = utils.check_airport_medium(am_name1, am_min_stop1,
                                                             am_max_stop1, airline, am_airport1, id)
                        if am_msg1 == 'success':
                            try:
                                utils.add_airport_medium(am_name1, am_min_stop1,
                                                         am_max_stop1, am_description1,
                                                         id, am_airport1)
                            except:
                                am_msg1 = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'

                        if am_number == '2':
                            am_name2 = request.form['name-stop2']
                            am_min_stop2 = request.form['time-stop-min2']
                            am_max_stop2 = request.form['time-stop-max2']
                            am_description2 = request.form['description2']
                            am_airport2 = form.airports2.data
                            am_msg2 = utils.check_airport_medium(am_name2, am_min_stop2,
                                                             am_max_stop2, airline, am_airport2, id)
                            if am_msg2 == 'success':
                                try:
                                    utils.add_airport_medium(am_name2, am_min_stop2,
                                                             am_max_stop2, am_description2,
                                                             id, am_airport2)
                                except:
                                    am_msg2 = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
                    else:
                        sts_msg = 'Không có số lượng sân bay trung gian'
            except:
                sts_msg = "success"



        return self.render('admin/flight.html', form=form,
                           sts_msg=sts_msg, am_msg1=am_msg1, am_msg2=am_msg2)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        pass

    @expose('/details/')
    def details_view(self):
        pass

    @expose('/delete/', methods=('POST',))
    def delete_view(self):
        pass


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for("index"))


admin.add_view(FlightManagementView(Flight, db.session, name="Quản lý chuyến bay", endpoint='flights'))
admin.add_view(RegulationView(Regulation, db.session, name='Quy định'))
admin.add_view(StatsView(name="Thống kê báo cáo"))
admin.add_view(LogoutView(name="Đăng xuất"))
