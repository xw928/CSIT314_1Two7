from flask import Blueprint, render_template, request, jsonify, session
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
from controller.buyer.getSpecificCarDetailController import getSpecificCarDetailController

buyer_blueprint = Blueprint('buyer_blueprint', __name__)

# For navigate to specific page
@buyer_blueprint.route('/buyer_home')
def buyer_dashboard():
    return render_template('Buyer/buyerDashboard.html', current_page='dashboard')


#70 As a Buyer, I want to search for used cars available for sale so that I can explore different car options using keywords.
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


#71 As a Buyer, I want to view the used car listings available for sale so that I can access used car information.
@buyer_blueprint.route('/buyer_ucl', methods=['GET'])
def displayViewAvailableUsedCarList():
    if request.method == 'GET':
        cars_info = getAvailableUsedCarListController().getAvailableUsedCarList()
        session['cars_info'] = cars_info 
        if cars_info:
            return render_template('Buyer/viewAvailableUsedCarList.html', cars_info=cars_info)
        else:
            message = "No Used Car Listing Found..."
            return render_template('Buyer/viewAvailableUsedCarList.html', message=message)


#72 As a Buyer, I want to save the cars that I’m interested in on my shortlist so that I can easily access them again later.
@buyer_blueprint.route('/shortlist_car', methods=['POST'])
def displayBuyerAddToShortList():
    car_id = request.form.get('car_id') 
    buyer_username = session.get('username')  
    car_info = getSpecificCarDetailController().getSpecificCarDetail(car_id)
    
    is_added = addToBuyerShortListController().addBuyerShortList(buyer_username, car_id)

    if is_added:
        car_info = getSpecificCarDetailController().getSpecificCarDetail(car_id)
        message = "Car has been successfully shortlisted!"
        message_type = "success"
    else:
        message = "Car has already been shortlisted!"
        message_type = "error"
    return render_template('Buyer/viewCarDetail.html', message=message, message_type=message_type, car_info=car_info)


#73 As a Buyer, I want to view the car in my shortlist so that I can view information of the shortlisted cars that I’m interested in.
@buyer_blueprint.route('/buyer_sl')
def displayViewBuyerShortlist():
    buyer_username = session.get('username')
    if request.method == 'GET':
        cars_info = viewBuyerShortListedCarController().viewShortListedCar(buyer_username)

        if cars_info:
            return render_template('Buyer/shortlist.html', cars_info=cars_info, current_page='shortlist')
        else:
            message = "No Used Car Listings Found in your shortlist..."
            return render_template('Buyer/shortlist.html', message=message, current_page='shortlist')



#74 As a Buyer, I want to search for the cars I have shortlisted so that I can quickly find and review the details of my preferred options using keywords.
@buyer_blueprint.route('/search_sl', methods=['GET', 'POST'])
def displaySearchBuyerShortList():
    buyer_username = session.get('username')

    if request.method == 'POST':
        field = request.form.get('field')
        value = request.form.get('target')

        if not field or not value:
            message = "Please provide both a search field and a value."
            return render_template('Buyer/searchShortList.html', message=message)

        cars_info = searchBuyerShortListController().searchBuyerShortList(buyer_username, field, value)
        
        if cars_info:
            return render_template('Buyer/searchShortList.html', cars_info=cars_info)
        else:
            message = "No cars match your criteria in the shortlist."
            return render_template('Buyer/searchShortList.html', cars_info=[], message=message)
    
    return render_template('Buyer/searchShortList.html')


#75 As a Buyer, I want to submit a review of my experience working with a Used Car Agent so that I can share my feedback about their service with others.
#76 As a Buyer, I want to submit a rating for the Used Car Agent so that I can express my satisfaction with their service.
@buyer_blueprint.route('/buyer_fb', methods=['GET', 'POST'])
def displayBuyerSubmitFeedback():
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


#77 As a Buyer, I want to view all Used Car Agent reviews so that I can evaluate their service.
#78 As a Buyer, I want to view all Used Car Agent ratings so that I can evaluate their service.
@buyer_blueprint.route('/view_rr', methods=['GET'])
def displayViewAgentFeedback():
    if request.method == 'GET':
        ratings_info = viewAgentRatingController().getAllAgentRating()
        reviews_info = viewAgentReviewController().getAllAgentReview()

        if not ratings_info and not reviews_info:
            return render_template('Buyer/viewAgentRR.html', message="No Feedback Found")

        feedback_info = []

        for rating, review in zip(ratings_info, reviews_info):
            feedback_info.append({
                "agent_username": rating.get('agent_username'),
                "rating": rating.get('rating'),
                "review": review.get('review')
                })
        print(feedback_info)
        return render_template('Buyer/viewAgentRR.html', feedback_info=feedback_info)


#258 As a Buyer, I want to use a loan calculator so that I can estimate my monthly payments and determine if the used car fits within my budget.
@buyer_blueprint.route('/loan_calculator')
def displayBuyerLoanCalculator():
    return render_template('Buyer/loancalculator.html')


# for update view +1
@buyer_blueprint.route('/buyer_cd', methods=['GET'])
def getUsedCarDetail():
    car_id = request.args.get('car_id')
    car_info = []

    isAddView = updateUsedCarViewController().updateUsedCarView(car_id)

    if isAddView:
        car_info = getSpecificCarDetailController().getSpecificCarDetail(car_id)
        return render_template('Buyer/viewCarDetail.html', car_info=car_info)




