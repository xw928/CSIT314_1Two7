from flask import Blueprint, render_template, request, session
from controller.agent.createUsedCarListController import createUsedCarListController
from controller.agent.viewUsedCarListController import viewUsedCarListController
from controller.agent.updateUsedCarListController import updateUsedCarListController
from controller.agent.deleteUsedCarListController import deleteUsedCarListController
from controller.agent.searchAgentUsedCarListController import searchAgentUsedCarListController
from controller.agent.getRatingController import getRatingController
from controller.agent.getReviewController import getReviewController

agent_blueprint = Blueprint('agent_blueprint', __name__)

# For navigate to Home Page
@agent_blueprint.route('/agent_home')
def agent_dashboard():
    return render_template('Agent/agentDashboard.html', current_page='dashboard')


#40 As a Used Car Agent, I want to create a used car listing so that buyers can view the used car's information.
@agent_blueprint.route('/create_car', methods=['GET','POST'])
def displayCreateUsedCarList():
    agent_username = session.get('username')

    if request.method == 'POST':
        seller_username = request.form['seller_username']
        car_type = request.form['car_type']
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        fuel_type = request.form['fuel_type']
        mileage = request.form['mileage']
        transmission = request.form['transmission']
        engine_size = request.form['engine_size']
        description = request.form['description']

        isAdded = createUsedCarListController().createUsedCarList(agent_username, seller_username, car_type, brand, model, year, price, fuel_type, mileage, transmission, engine_size, description)

        if isAdded:
            message = "Used Car Listing Created Successfully!"
            message_type = "success"
        else:
            message = "Failed to create the used car listing. Please check the details and try again."
            message_type = "error"
        return render_template('Agent/createList.html', message=message, message_type=message_type)
    
    return render_template('Agent/createList.html')


#41 As a Used Car Agent, I want to view used car listings I put up so that I can stay updated on their status.
@agent_blueprint.route('/view_car', methods=['GET'])
def displayViewUsedCarList():
    agent_username = session.get('username')
    if request.method == 'GET':
        cars_info = viewUsedCarListController().viewUsedCarList(agent_username)
        session['cars_info'] = cars_info 
        if cars_info:
            return render_template('Agent/viewList.html', cars_info=cars_info)
        else:
            message = "No Used Car Listing Found..."
            return render_template('Agent/viewList.html', message=message)
    
    
#42 As a Used Car Agent, I want to update used car listings so that the latest used car information is available.
@agent_blueprint.route('/update_car', methods=['GET', 'POST'])
def displayUpdateUsedCarList():
    message = None  
    car_id = 0
    car_info = None 
    if request.method == 'GET':
        car_id = request.args.get('car_id')
        if car_id:
            car_id = int(car_id)  # Convert car_id to an integer for proper comparison
            cars_info = session.get('cars_info')
            if cars_info:  # Check if cars_info exists in the session
                car_info = next((car for car in cars_info if car['car_id'] == car_id), None)
            session.pop("cars_info", None)
        return render_template('Agent/updateList.html', car_info=car_info)

    elif request.method == 'POST':
        car_id = request.form['car_id']
        new_seller_username = request.form['new_seller_username']
        new_car_type = request.form['new_car_type']
        new_brand = request.form['new_brand']
        new_model = request.form['new_model']
        new_year = request.form['new_year']
        new_price = request.form['new_price']
        new_fuel_type = request.form['new_fuel_type']
        new_mileage = request.form['new_mileage']
        new_transmission = request.form['new_transmission']
        new_engine_size = request.form['new_engine_size']
        new_description = request.form['new_description']
        new_status = request.form['new_status']

        isUpdated = updateUsedCarListController().updateUsedCarList(car_id, new_seller_username, new_car_type, new_brand, new_model, new_year, new_price, new_fuel_type, new_mileage, new_transmission, new_engine_size, new_description, new_status)

        if isUpdated:
            message = "Used Car Listing Updated Successfully!"
            message_type = "success"
        else:
            message = "Failed to update the used car listing. Please check the details and try again."
            message_type = "error"
            return render_template('Agent/updateList.html', message=message, message_type=message_type, car_info=car_info)

    session.pop("car_info", None)
    return render_template('Agent/updateList.html', message=message, message_type=message_type)


#43 As a Used Car Agent, I want to delete used car listings so that I can remove sold used cars or sellers change their minds from the database.
@agent_blueprint.route('/delete_car', methods=['GET', 'POST'])
def displayDeleteUsedCarList():
    message = None
    car_id = 0
    car_info = None 
    if request.method == 'GET':
        car_id = request.args.get('car_id')
        if car_id:
            car_id = int(car_id)  
            cars_info = session.get('cars_info')
            if cars_info:  
                car_info = next((car for car in cars_info if car['car_id'] == car_id), None)
            session.pop("cars_info", None)
        return render_template('Agent/deleteList.html', car_info=car_info)
    
    elif request.method == "POST":
        car_id = request.form['car_id']
        isDeleted = deleteUsedCarListController().deleteUsedCarList(car_id)

        if isDeleted:
            message = "Used Car Listing Deleted Successfully!"
    
    session.pop("car_info", None)
    return render_template('Agent/deleteList.html', message=message, car_info=car_info)
        

#44 As a Used Car Agent, I want to search for used car listings so that I can efficiently find a suitable used car that matches the buyer.
@agent_blueprint.route('/search_car', methods=['GET', 'POST'])
def displaySearchUsedCarList():
    agent_username = session.get('username')

    if request.method == 'POST':
        field = request.form.get('field')
        value = request.form.get('target')

        cars_info = searchAgentUsedCarListController().searchAgentUsedCarList(agent_username, field, value)
        if cars_info:
            return render_template('Agent/searchList.html', cars_info=cars_info)
        else:
            message = "Used Car Listing Not Found..."
        return render_template('Agent/searchList.html', user_info=[], message=message)
    
    return render_template('Agent/searchList.html')


#45 As a Used Car Agent, I want to view my ratings so that I can see how satisfied my clients are and improve my services.
#46 As a Used Car Agent, I want to view my reviews so that I can understand my clients' feedback and improve my service accordingly.
@agent_blueprint.route('/agent_feedback', methods=['GET'])
def displayAgentFeedbackPage():
    agent_username = session.get('username')
    if request.method == 'GET':
        ratings_info = getRatingController().getRating(agent_username)
        reviews_info = getReviewController().getReview(agent_username)

        if not ratings_info and not reviews_info:
            return render_template('Agent/agentFeedback.html', message="No Feedback Found", current_page='agent_feedback')
        
        feedback_info = []
        for rating, review in zip(ratings_info, reviews_info):
            feedback_info.append({"sender_id":rating['sender_id'],"rating":rating['rating'],"review":review['review']})

        return render_template('Agent/agentFeedback.html', feedback_info=feedback_info, current_page='agent_feedback')       