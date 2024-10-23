from flask import Blueprint, render_template

used_car_agent_blueprint = Blueprint('used_car_agent_blueprint', __name__)

@used_car_agent_blueprint.route("/agent/dashboard")
def admin_dashboard():
    return "this is used car agent dashboard"