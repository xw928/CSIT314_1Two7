from flask import Blueprint, render_template, request, url_for, redirect, session
from controller.user.loginController import loginController
from controller.user.resetPasswordController import resetPasswordController
from controller.admin.createAccountController import createAccountController

user_view_blueprint = Blueprint('user_view_blueprint', __name__)


#6 As a User Admin, I want to log into the system so that I can perform administrative tasks and manage the user's account.
#38 As a Used Car Agent, I want to log into the used car platform so that I can access my account and manage used car listings. 
#68 As a Buyer, I want to log into the used car platform so that I can access my account and view, search, and save used car listings.
#79 As a Seller, I want to log into the used car platform so that I can access my account and track my interest in my used car.
@user_view_blueprint.route("/", methods=['GET', 'POST'])
def displayLoginPage():

    if request.method == "GET":
        return render_template("User/userLogin.html")
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user_info = loginController().verifyAccount(username,password)

        if user_info:
            session["loggedIn"] = True
            session["username"] = user_info['username']
            session["role"] = user_info['profile_id']
            return redirect(url_for("user_view_blueprint.displayDashboard"))
        else:
            return render_template("User/userLogin.html", message="Invalid username or password, Please try again.")



@user_view_blueprint.route('/dashboard', methods=['GET'])
def displayDashboard():
    if "loggedIn" in session:
        if session['role'] == 1:
            return render_template('Admin/adminDashboard.html', current_page='dashboard')
        elif session['role'] == 2:
            return render_template('Agent/agentDashboard.html', current_page='dashboard')
        elif session['role'] == 3:
            return render_template('Buyer/buyerDashboard.html', current_page='dashboard')
        elif session['role'] == 4:
            return render_template('Seller/sellerDashboard.html', current_page='dashboard')
        else:
            return redirect(url_for("user_view_blueprint.displayLoginPage"))
           
    return redirect(url_for("user_view_blueprint.displayLoginPage"))



#7 As a User Admin, I want to log out the system so that I can exit the system when I am not using it.
#39 As a Used Car Agent, I want to log out of my account so that I can exit the platform when I am not using it.
#69 As a Buyer, I want to log out of my account so that I can exit the platform when I am not using it.
#80 As a Seller, I want to log out of my account so that I can exit the platform when I am not using it.
@user_view_blueprint.route("/logout", methods=["POST"])
def displayLogout():
    session.clear()
    return redirect('/')



@user_view_blueprint.route('/reset_pwd', methods=['GET', 'POST'])
def displayResetPassword():
    if request.method == 'POST':
        username = request.form["username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return render_template('User/resetPassword.html',message='Password Mismatch!', message_type="error")

        isReset = resetPasswordController().resetUserPassword(username, new_password)

        if isReset:
            message = "Your password has been reset successfully!"
            message_type = "success"
        else:
            message = "Failed - Invalid Username"
            message_type = "error"
        return render_template('User/resetPassword.html', message=message, message_type=message_type)
        
    return render_template('User/resetPassword.html')



@user_view_blueprint.route('/sign-up', methods=['GET', 'POST'])
def displaySignUpAccount():    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        profile_id = request.form['profile_id']
        
        isAdded = createAccountController().createUserAccount(username, password, profile_id)

        if isAdded:
            message = "Sign Up Successfully!"
            message_type = "success"
        else:
            message = "Username is taken. Please choose another."
            message_type = "error"
        return render_template('User/signUpAccount.html', message=message, message_type=message_type)
    
    return render_template('User/signUpAccount.html')

