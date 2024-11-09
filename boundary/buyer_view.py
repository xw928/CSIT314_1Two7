from flask import Blueprint, render_template, request, jsonify, session
# from controller.user.loginController import LoginController

from controller.buyer.searchAvailableUsedCarListController import searchAvailableUsedCarListController
from controller.buyer.buyerSubmitRatingController import buyerSubmitRatingController
from controller.buyer.buyerSubmitReviewController import buyerSubmitReviewController
from controller.buyer.viewAgentRatingController import viewAgentRatingController
from controller.buyer.viewAgentReviewController import viewAgentReviewController
from controller.buyer.getAvailableUsedCarListController import getAvailableUsedCarListController
from controller.buyer.updateUsedCarViewController import updateUsedCarViewController
from controller.buyer.addToBuyerShortListController import addToBuyerShortListController
from controller.buyer.viewBuyerShortListedCarController import viewBuyerShortListedCarController
from controller.buyer.searchBuyerShortListController import searchBuyerShortListController


buyer_blueprint = Blueprint('buyer_blueprint', __name__)

# For navigate to specific page
@buyer_blueprint.route('/buyer_home')
def buyer_dashboard():
    return render_template('Buyer/buyerDashboard.html', current_page='dashboard')

@buyer_blueprint.route('/buyer_sl')
def buyer_shortlist():
    buyer_username = session.get('username')
    if request.method == 'GET':
        # Call the viewShortListedCar method to get the car information
        cars_info = viewBuyerShortListedCarController().viewShortListedCar(buyer_username)

        if cars_info:
            # If there are cars in the shortlist, render the template with the car details
            return render_template('Buyer/shortlist.html', cars_info=cars_info, current_page='shortlist')
        else:
            # If no cars were found, show a message
            message = "No Used Car Listings Found in your shortlist..."
            return render_template('Buyer/shortlist.html', message=message, current_page='shortlist')



@buyer_blueprint.route('/buyer_fb')
def buyer_feedback():
    return render_template('Buyer/buyerFeedback.html', current_page='feedback')

@buyer_blueprint.route('/loan_calculator')
def buyer_loancalculator():
    return render_template('Buyer/loancalculator.html', current_page='loancalculator')

@buyer_blueprint.route('/buyer_ucl', methods=['GET'])
def getAvailableUsedCarList():
    if request.method == 'GET':
        cars_info = getAvailableUsedCarListController().getAvailableUsedCarList()
        session['cars_info'] = cars_info 
        if cars_info:
            return render_template('Buyer/viewAvailableUsedCarList.html', cars_info=cars_info)
        else:
            message = "No Used Car Listing Found..."
            return render_template('Buyer/viewAvailableUsedCarList.html', message=message)

@buyer_blueprint.route('/buyer_cd', methods=['GET'])
def getUsedCarDetail():
    car_id = request.args.get('car_id')

    if car_id:
        # Update the view count
        isAddView = updateUsedCarViewController().updateUsedCarView(car_id)

        if isAddView:
            print(f"View count for car {car_id} updated successfully.")

        cars_info = session.get('cars_info')

        car_info = next((car for car in cars_info if car["car_id"] == int(car_id)), None)

        if car_info:
            car_info['view'] += 1
            session['cars_info'] = cars_info 

        return render_template('Buyer/viewCarDetail.html', car_info=car_info)

    return render_template('Buyer/viewCarDetail.html')


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
        return render_template('Buyer/buyerFeedback.html', message=message, message_type=message_type, current_page='feedback')
    return render_template('Buyer/buyerFeedback.html', current_page='feedback')

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
    
@buyer_blueprint.route('/shortlist_car', methods=['POST'])
def addBuyerShortList():
    car_id = request.form.get('car_id')  # Get the car_id from the form data (passed by the button)
    buyer_username = session.get('username')  # Get the buyer_username from the session (assuming it's stored)
    
    # Call the method to add the car to the shortlist
    is_added = addToBuyerShortListController().addBuyerShortList(buyer_username, car_id)
    
    # Fetch the car details after attempting to add to the shortlist
    cars_info = session.get('cars_info')
    car_info = next((car for car in cars_info if car["car_id"] == int(car_id)), None)

    if is_added:
        car_info['shortlisted'] += 1
        session['cars_info'] = cars_info
        message = "Car has been successfully shortlisted!"
        message_type = "success"
    else:
        message = "Car has already been shortlisted!"
        message_type = "error"
    
    # Return to the view with the appropriate message
    return render_template('Buyer/viewCarDetail.html', message=message, message_type=message_type, car_info=car_info)

@buyer_blueprint.route('/search_sl', methods=['GET', 'POST'])
def searchBuyerShortList():
    # Ensure the buyer's username is pulled from the session
    buyer_username = session.get('buyer_username')

    if request.method == 'POST':
        field = request.form.get('field')
        value = request.form.get('target')

        # Check if the 'field' and 'value' are provided
        if not field or not value:
            message = "Please provide both a search field and a value."
            return render_template('Buyer/searchShortList.html', message=message)

        # Pass the session's buyer_username to the entity function
        cars_info = searchBuyerShortListController().searchBuyerShortList(field, value, buyer_username)
        
        # Check if cars_info is empty and display appropriate message
        if cars_info:
            return render_template('Buyer/searchShortList.html', cars_info=cars_info)
        else:
            message = "No cars match your criteria in the shortlist."
            return render_template('Buyer/searchShortList.html', cars_info=[], message=message)
    
    return render_template('Buyer/searchShortList.html')


