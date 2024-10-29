from flask import Blueprint, render_template, request, jsonify
# from controller.user.loginController import LoginController

seller_blueprint = Blueprint('seller_blueprint', __name__)

# For navigate to specific page
@seller_blueprint.route('/seller_home')
def seller_dashboard():
    return render_template('Seller/sellerDashboard.html', current_page='dashboard')

@seller_blueprint.route('/seller_fb')
def seller_feedback():
    return render_template('Seller/sellerFeedback.html', current_page='seller_fb')