from FlightManagement.admin import *
from FlightManagement import app, login, utils, controllers


app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/', 'login', controllers.login_my_user, methods=['get','post'])
app.add_url_rule('/logout', 'logout', controllers.login_my_user)
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/api/airport_info', 'add-flight', controllers.airports)



@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)