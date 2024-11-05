from flask import Blueprint, render_template, request, jsonify, session
# from controller.user.loginController import LoginController

from controller.buyer.searchAvailableUsedCarListController import searchAvailableUsedCarListController
from controller.buyer.buyerSubmitRatingController import buyerSubmitRatingController
from controller.buyer.buyerSubmitReviewController import buyerSubmitReviewController
from controller.buyer.viewAgentRatingController import viewAgentRatingController
from controller.buyer.viewAgentReviewController import viewAgentReviewController


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

@buyer_blueprint.route('/buyer_search_car', methods=['GET', 'POST'])
def displaySearchUsedCarList():

    if request.method == 'POST':
        field = request.form.get('field')
        value = request.form.get('target')

        cars_info = searchAvailableUsedCarListController().searchAvailableUsedCarList(field, value)
        if cars_info:
            return render_template('Buyer/searchList.html', cars_info=cars_info)
        else:
            message = "Used Car Listing Not Found..."
        return render_template('Buyer/searchList.html', user_info=[], message=message)
    
    return render_template('Buyer/searchList.html')


@buyer_blueprint.route('/buyer_fb', methods=['GET', 'POST'])
def display_buyer_submit_feedback():
    buyer_username = session.get('username')
    if request.method == "POST":
       
        agent_username = request.form["agent_username"]
        buyer_rating = request.form["rating"]
        buyer_review = request.form["review"]

        submitRating = buyerSubmitRatingController().submitRating(agent_username, buyer_username, buyer_rating)
        submitReview = buyerSubmitReviewController().submitReview(agent_username, buyer_username, buyer_review)


        if submitRating and submitReview:
            message = "Feedback Submitted Successfully!"
            message_type = "success"
        else:
            message = "Agent Username does not exists. Please try again..."
            message_type = "error"
        return render_template('Buyer/buyerFeedback.html', message=message, message_type=message_type, current_page='buyer_fb')
    return render_template('Buyer/buyerFeedback.html', current_page='buyer_fb')


@buyer_blueprint.route('/view_rr', methods=['GET'])
def displayViewAgentRR():
    if request.method == 'GET':
        ratings_info = viewAgentRatingController().getAllAgentRating()
        reviews_info = viewAgentReviewController().getAllAgentReview()

        if not ratings_info and not reviews_info:
            return render_template('Buyer/viewAgentRR.html', message="No Feedback Found", current_page='view_rr')
        
        feedback_info = []

        for rating, review in zip(ratings_info, reviews_info):
            feedback_info.append({
                "agent_username": rating.get('agent_username'),
                "rating": rating.get('rating'),
                "review": review.get('review')
                })
            
        return render_template('Buyer/viewAgentRR.html', feedback_info=feedback_info, current_page='view_rr')  