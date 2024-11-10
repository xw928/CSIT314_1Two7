from flask import Blueprint, render_template, request, jsonify, url_for, redirect, session
from controller.seller.sellerSubmitRatingController import sellerSubmitRatingController
from controller.seller.sellerSubmitReviewController import sellerSubmitReviewController
from controller.seller.sellerViewUsedCarController import sellerViewUsedCarListController
from controller.seller.sellerSearchUsedCarListController import sellerSearchUsedCarListController
from controller.seller.getAllAgentRatingController import getAllAgentRatingController
from controller.seller.getAllAgentReviewController import getAllAgentReviewController

seller_blueprint = Blueprint('seller_blueprint', __name__)

# For navigate to specific page
@seller_blueprint.route('/seller_home')
def seller_dashboard():
    return render_template('Seller/sellerDashboard.html', current_page='dashboard')


#81 As a Seller, I want to view all my used cars so that I can easily manage and track the used cars I own.
#83 As a Seller, I want to track the number of views on my used car so that I can gauge the level of interest from potential buyers
#84 As a Seller, I want to track how many times my used cars are shortlisted so that I can know which cars are generating the most interest.
@seller_blueprint.route('/seller_view_car', methods=['GET'])
def displayViewUsedCarList():
    seller_username = session.get('username')

    if request.method == 'GET':
        cars_info = sellerViewUsedCarListController().viewUsedCarList(seller_username)
        session['cars_info'] = cars_info 

        if cars_info:
            return render_template('Seller/sellerViewList.html', cars_info=cars_info)
        else:
            message = "No Used Car Listing Found..."
            return render_template('Seller/sellerViewList.html', message=message)


#82 As a Seller, I want to search my used car listings so that I can easily find my used car using keywords
@seller_blueprint.route('/seller_search_car', methods=['GET', 'POST'])
def displaySearchUsedCarList():
    seller_username = session.get('username')

    if request.method == 'POST':
        field = request.form.get('field')
        value = request.form.get('target')

        cars_info = sellerSearchUsedCarListController().sellerSearchUsedCarList(seller_username, field, value)
        if cars_info:
            return render_template('Seller/sellerSearchList.html', cars_info=cars_info)
        else:
            message = "Used Car Listing Not Found..."
        return render_template('Seller/sellerSearchList.html', user_info=[], message=message)
    
    return render_template('Seller/sellerSearchList.html') 
    

#85 As a Seller, I want to view all Used Car Agent reviews so that I can evaluate their service.
#267 As a Seller, I want to view all Used Car Agent ratings so that I can evaluate their service.
@seller_blueprint.route('/seller_feedback', methods=['GET'])
def displaySellerViewAgentFeedbackPage():
    if request.method == 'GET':
        ratings_info = getAllAgentRatingController().getAllAgentRating()
        reviews_info = getAllAgentReviewController().getAllAgentReview()
        
        # Check if there is no feedback data
        if not ratings_info and not reviews_info:
            return render_template('Seller/viewAgentFeedback.html', message="No Feedback Found", current_page='seller_feedback')
        
        feedback_info = []
        
        # Only proceed if both ratings and reviews have data
        for rating, review in zip(ratings_info, reviews_info):
            feedback_info.append({
                "agent_username": rating.get('agent_username'), 
                "rating": rating.get('rating'), 
                "review": review.get('review')
            })

        return render_template('Seller/viewAgentFeedback.html', feedback_info=feedback_info, current_page='seller_feedback')

#86 As a Seller, I want to submit a review of my experience working with a Used Car Agent so that I can share my feedback about their service with others.
#87 As a Seller, I want to submit a rating for the Used Car Agent so that I can express my satisfaction with their service.
@seller_blueprint.route('/seller_fb', methods=['GET', 'POST'])
def displaySellerSubmitFeedback():
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




