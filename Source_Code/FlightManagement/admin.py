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
    edit_modal = True
    details_modal = True
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

            sts_msg = utils.check_flight(id, name, departing_at, arriving_at, plane, airline)


        return self.render('admin/flight.html', form=form, sts_msg=sts_msg)


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
