from flask import Flask

app = Flask(__name__, template_folder="FrontEnd")

from boundary.user_admin import user_admin_blueprint
app.register_blueprint(user_admin_blueprint)

from boundary.used_car_agent import used_car_agent_blueprint
app.register_blueprint(used_car_agent_blueprint)

if __name__ == '__main__':
    app.run(debug=True)