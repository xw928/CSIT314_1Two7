from flask import Flask
from datetime import timedelta

app = Flask(__name__, template_folder="FrontEnd")

app.secret_key = "123"
app.permanent_session_lifetime = timedelta(days=7)

from boundary.user_view import user_view_blueprint
app.register_blueprint(user_view_blueprint)

from boundary.admin_view import admin_blueprint
app.register_blueprint(admin_blueprint)

from boundary.agent_view import agent_blueprint
app.register_blueprint(agent_blueprint)

from boundary.buyer_view import buyer_blueprint
app.register_blueprint(buyer_blueprint)

from boundary.seller_view import seller_blueprint
app.register_blueprint(seller_blueprint)


if __name__ == '__main__':
    app.run(debug=True)