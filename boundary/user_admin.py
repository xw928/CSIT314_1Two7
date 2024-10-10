from flask import Blueprint, render_template

user_admin_blueprint = Blueprint('user_admin', __name__)

@user_admin_blueprint.route("/")
def admin_dashboard():
    return "this is admin dashboard"

@user_admin_blueprint.route("/login")
def admin_login():
    return render_template("admin/adminLogin.html")
