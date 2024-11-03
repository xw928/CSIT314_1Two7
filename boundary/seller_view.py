from flask import Blueprint, render_template, request, jsonify, url_for, redirect, session
from controller.seller.sellerSubmitRatingController import sellerSubmitRatingController
from controller.seller.sellerSubmitReviewController import sellerSubmitReviewController

seller_blueprint = Blueprint('seller_blueprint', __name__)

# For navigate to specific page
@seller_blueprint.route('/seller_home')
def seller_dashboard():
    return render_template('Seller/sellerDashboard.html', current_page='dashboard')

@seller_blueprint.route('/seller_fb', methods=['GET', 'POST'])
def display_seller_submit_feedback():
    sender_username = session.get('username')
    if request.method == "POST":
       
        agent_username = request.form["agent_username"]
        seller_rating = request.form["rating"]
        seller_review = request.form["review"]

        submitRating = sellerSubmitRatingController().submitRating(agent_username, sender_username, seller_rating)
        submitReview = sellerSubmitReviewController().submitReview(agent_username, sender_username, seller_review)


        if submitRating and submitReview:
            message = "Feedback Submitted Successfully!"
            message_type = "success"
        else:
            message = "Agent Username does not exists. Please try again..."
            message_type = "error"
        return render_template('Seller/sellerFeedback.html', message=message, message_type=message_type, current_page='seller_fb')
    return render_template('Seller/sellerFeedback.html', current_page='seller_fb')

