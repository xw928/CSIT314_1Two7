from flask import Blueprint, render_template, request, jsonify
# from controller.user.loginController import LoginController

admin_blueprint = Blueprint('admin_blueprint', __name__)

@admin_blueprint.route('/admin_home')
def admin_dashboard():
    return render_template('Admin/adminDashboard.html')

@admin_blueprint.route('/user_acc')
def user_account():
    return render_template("Admin/UserAccount.html")

@admin_blueprint.route('/user_pf')
def user_profile():
    return render_template('Admin/UserProfile.html')

# @user_admin_blueprint.route("/")
# def login_page():
#     return render_template("login.html")

# @user_admin_blueprint.route("/login", methods=['POST'])
# def admin_login():

#     username = request.form['username']
#     password = request.form['password']

    

#     isUserValid = LoginController().loginController(username,password)

#     if not isUserValid:
#         return jsonify(success=isUserValid, message="User not existed pls enter again")

#     # print(f'username: {username}  password: {password}')

#     print(f'{isUserValid}')

#     return jsonify(success=isUserValid, message="User is Valid!!!")

    
