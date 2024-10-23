from flask import Blueprint, render_template, request, jsonify, url_for, redirect, session
from controller.user.loginController import loginController

user_view_blueprint = Blueprint('user_view_blueprint', __name__)

@user_view_blueprint.route("/", methods=['GET', 'POST'])
def displayLoginPage():

    if request.method == "GET":
        if "loggedIn" in session:
            return redirect(url_for("user_view_blueprint.displayDashboard"))
        return render_template("User/userLogin.html")
    
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        user_info = loginController().verifyAccount(username,password)

        if user_info:
            session["loggedIn"] = True
            session["username"] = user_info['username']
            session["role"] = user_info['role']
            return redirect(url_for("user_view_blueprint.displayDashboard"))
        else:
            return render_template("User/userLogin.html", message="Invalid username or password, Please try again.")
            


@user_view_blueprint.route("/logout", methods=["POST"])
def displayLogout():
    session.clear()
    return redirect('/')


@user_view_blueprint.route('/dashboard', methods=['Get'])
def displayDashboard():

    if "loggedIn" in session:
           
        if session['role'] == "admin":
            return render_template('Admin/adminDashboard.html')
        elif session['role'] == "agent":
            return render_template('Agent/agentDashboard.html')
        elif session['role'] == "buyer":
            return render_template('Buyer/buyerDashboard.html')
        elif session['role'] == "seller":
            return render_template('Seller/sellerDashboard.html')
        
    return redirect(url_for("user_view_blueprint.displayLoginPage"))



    
