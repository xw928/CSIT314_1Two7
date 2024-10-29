from flask import Blueprint, render_template, request, jsonify
# from controller.user.loginController import LoginController

agent_blueprint = Blueprint('agent_blueprint', __name__)

# For navigate to specific page
@agent_blueprint.route('/agent_home')
def agent_dashboard():
    return render_template('Agent/agentDashboard.html', current_page='dashboard')

@agent_blueprint.route('/agent_fb')
def agent_feedback():
    return render_template('Agent/agentFeedback.html', current_page='agent_fb')