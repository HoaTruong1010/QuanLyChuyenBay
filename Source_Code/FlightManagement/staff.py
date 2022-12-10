# from FlightManagement import staff, db
# from FlightManagement.models import *
# from flask_admin.contrib.sqla import ModelView

# class UserView(ModelView):
#     column_display_pk = True
#     can_view_details = True
#     can_export = True
#     edit_modal = True
#     details_modal = True
#     column_filters = ['name', 'user_role']
#     column_searchable_list = ['id', 'name', 'username', 'user_role']
#     column_exclude_list = ['password']
#     column_labels = {
#         'id': 'ID',
#         'name': 'Họ và tên',
#         'username': 'Username',
#         'active': 'Trạng thái hoạt động',
#         'joined_date': 'Ngày tạo',
#         'user_role': 'Vai Trò'
#     }


# staff.add_view(ModelView(User, db.session, name='Tất cả tài khoản'))