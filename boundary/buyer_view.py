from flask import Blueprint, render_template, request, jsonify
# from controller.user.loginController import LoginController

buyer_blueprint = Blueprint('buyer_blueprint', __name__)

# For navigate to specific page
@buyer_blueprint.route('/buyer_home')
def buyer_dashboard():
    return render_template('Buyer/buyerDashboard.html', current_page='dashboard')

@buyer_blueprint.route('/buyer_sl')
def buyer_shortlist():
    return render_template('Buyer/shortlist.html', current_page='shortlist')

@buyer_blueprint.route('/buyer_fb')
def buyer_feedback():
    return render_template('Buyer/buyerFeedback.html', current_page='feedback')