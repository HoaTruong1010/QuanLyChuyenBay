from flask import redirect, url_for, request, flash
from flask_admin import Admin, expose, BaseView
from flask_admin.babel import gettext, ngettext
from flask_admin.helpers import get_redirect_target, flash_errors
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_login import current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import SelectField

from FlightManagement import utils, controllers

from FlightManagement import app, db
from FlightManagement.models import *
from flask_admin.contrib.sqla import ModelView

admin = Admin(app=app, name="AFFORDA", template_mode="bootstrap4")


class Base_View(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    # edit_modal = True
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
    planes = SelectField('planes', choices=[])
    airlines = SelectField('airlines', choices=[])


class FlightManagementView(AuthenticatedModelView):
    column_filters = ['name', 'id']
    column_searchable_list = ['name', 'id']
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
        am_msg = ''
        form = Form()
        form.planes.choices = [p.id for p in AirPlane.query.all()]
        form.airlines.choices = [a.name for a in AirLine.query.all()]

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
                    utils.save_flight(id, name, departing_at, arriving_at, plane, airline)
                except:
                    sts_msg = 'Đã có lỗi xảy ra khi lưu chuyến bay! Vui lòng quay lại sau!'

                try:
                    is_apm = request.form['isMedium']

                    if is_apm == 'on':
                        am_number = request.form['number']
                        num = int(am_number)
                        for i in range(num):
                            str_name = "name-stop-" + str(i)
                            str_stb = "stop-time-begin-" + str(i)
                            str_stf = "stop-time-finish-" + str(i)
                            str_des = "description-" + str(i)
                            str_ap = "form-select-" + str(i)

                            am_name = request.form[str_name]
                            am_stb = request.form[str_stb]
                            am_stf = request.form[str_stf]
                            am_des = request.form[str_des]
                            am_ap = request.form[str_ap]
                            am_msg = utils.check_airport_medium(am_name, am_stb,
                                                                 am_stf, airline, am_ap, id)
                            if am_msg == 'success':
                                try:
                                    utils.save_airport_medium(am_name, am_stb,
                                                             am_stf, am_des,
                                                             id, am_ap)
                                except:
                                    f = Flight.query.get(id)
                                    db.session.delete(f)
                                    db.session.commit()
                                    am_msg = 'Đã có lỗi xảy ra khi lưu sân bay trung gian! Vui lòng quay lại sau!'
                            else:
                                f = Flight.query.get(id)
                                db.session.delete(f)
                                db.session.commit()
                                am_msg = am_msg
                    else:
                        sts_msg = 'Không có số lượng sân bay trung gian'
                except:
                    sts_msg = "success"



        return self.render('admin/flight.html', form=form,
                           sts_msg=sts_msg, am_msg=am_msg)

    # @expose('/edit/', methods=('GET', 'POST'))
    # def edit_view(self):
    #     pass

    @expose('/details/')
    def details_view(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_view_details:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        apm_list = Flight_AirportMedium.query.filter(
            Flight_AirportMedium.flight_id.__eq__(id)
        ).all()

        return self.render("admin/flight-details.html",
                           model=model,
                           details_columns=self._details_columns,
                           get_value=self.get_detail_value,
                           apm_list=apm_list,
                           return_url=return_url)



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
admin.add_view(ModelView(Flight_AirportMedium, db.session, name='Trung gian'))
admin.add_view(StatsView(name="Thống kê báo cáo"))
admin.add_view(LogoutView(name="Đăng xuất"))
