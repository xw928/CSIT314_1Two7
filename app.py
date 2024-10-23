from flask import Flask
from datetime import timedelta

app = Flask(__name__, template_folder="FrontEnd")

# from boundary.user_admin import user_admin_blueprint
# app.register_blueprint(user_admin_blueprint)

app.secret_key = "123"
app.permanent_session_lifetime = timedelta(hours=1)

from boundary.user_view import user_view_blueprint
app.register_blueprint(user_view_blueprint)

from boundary.admin_view import admin_blueprint
app.register_blueprint(admin_blueprint)

# from boundary.used_car_agent import used_car_agent_blueprint
# app.register_blueprint(used_car_agent_blueprint)

if __name__ == '__main__':
    app.run(debug=True)