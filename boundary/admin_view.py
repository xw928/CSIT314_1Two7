from flask import Blueprint, render_template, request, session

from controller.admin.createAccountController import createAccountController
from controller.admin.viewAccountController import viewAccountController
from controller.admin.updateAccountController import updateAccountController
from controller.admin.suspendAccountController import suspendAccountController
from controller.admin.searchAccountController import searchAccountController

from controller.admin.createProfileController import createProfileController
from controller.admin.viewProfileController import viewProfileController
from controller.admin.updateProfileController import updateProfileController
from controller.admin.suspendProfileController import suspendProfileController
from controller.admin.searchProfileController import searchProfileController

admin_blueprint = Blueprint('admin_blueprint', __name__)

# For navigate to specific page
@admin_blueprint.route('/admin_home')
def displayAdminDashboard():
    return render_template('Admin/adminDashboard.html', current_page='dashboard')

@admin_blueprint.route('/user_acc')
def displayUserAccount():
    return render_template("Admin/UserAccount.html", current_page='user_account')

@admin_blueprint.route('/user_pf')
def displayUserProfile():
    return render_template('Admin/UserProfile.html', current_page='user_profile')


#8 As a User Admin, I want to create a user account so that I can grant access to the system for new users, allowing them to use the platform.
@admin_blueprint.route('/create_ua', methods=['GET','POST'])
def displayCreateUserAccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        profile_id = request.form['profile_id']

        isAdded = createAccountController().createUserAccount(username, password, profile_id)

        if isAdded:
            message = "User Account Created Successfully!"
            message_type = "success"
        else:
            message = "Username is taken. Please choose another."
            message_type = "error"
        return render_template('Admin/uaCreate.html', message=message, message_type=message_type)
    
    return render_template('Admin/uaCreate.html')


#9 As a User Admin, I want to create a user profile so that I can store and manage essential information, such as user type about each user.
@admin_blueprint.route('/create_up', methods=['GET','POST'])
def displayCreateUserProfile():
    if request.method == 'GET':
        return render_template('Admin/upCreate.html', isAdded=None)
    
    role = request.form['role']
    description = request.form['description']
    isAdded = createProfileController().createUserProfile(role, description)

    if isAdded:
        message = "User Profile Created Successfully!"
        message_type = "success"
    else:
        message = "The Role already exists. Please try again..."
        message_type = "error"
    return render_template('Admin/upCreate.html', message=message, message_type=message_type)


#10 As a User Admin, I want to view the user accounts so that I can know a user’s background.
@admin_blueprint.route('/view_ua', methods=['GET'])
def displayViewUserAccount():
    if request.method == 'GET':
        user_info = viewAccountController().viewUserAccount()
        return render_template('Admin/uaView.html', user_info=user_info)
    

#11 As a User Admin, I want to view the user profile so that I can know the user’s personal details.
@admin_blueprint.route('/view_up', methods=['GET'])
def displayViewUserProfile():
    if request.method == 'GET':
        profile_info = viewProfileController().viewUserProfile()
        return render_template('Admin/upView.html', profile_info=profile_info)
    

#12 As a User Admin, I want to update the user account so that the latest user account information is available.
@admin_blueprint.route('/update_ua', methods=['GET', 'POST'])
def displayUpdateUserAccount():
    message = None  

    if request.method == 'GET':
        user_info = session.get("user_info")
        return render_template('Admin/uaUpdate.html', user_info=user_info)

    elif request.method == 'POST':
        user_info = session.get("user_info")
        username = user_info['username'] if user_info else None
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        new_role = request.form["new_role"]
        new_status = request.form["new_status"]
        
        isUpdated = updateAccountController().updateUserAccount(username, new_username, new_password, new_role, new_status)

        if isUpdated:
            message = "User Account Updated Successfully!"
            message_type = "success"
        else:
            message = "Failed - Username already exists"
            message_type = "error"
            return render_template('Admin/uaUpdate.html', message=message, message_type=message_type, user_info=user_info)

    session.pop("user_info", None)
    return render_template('Admin/uaUpdate.html', message=message, message_type=message_type)


#13 As a User Admin, I want to update the user profile so that the latest user profile information is available.
@admin_blueprint.route('/update_up', methods=['GET', 'POST'])
def displayUpdateUserProfile():
    message = None 

    if request.method == 'GET':
        profile_info = session.get("profile_info")
        return render_template('Admin/upUpdate.html', profile_info=profile_info)

    elif request.method == 'POST':
        profile_info = session.get("profile_info")
        rolename = profile_info['role'] if profile_info else None
        new_rolename = request.form["new_rolename"]
        new_description = request.form["new_description"]
        new_status = request.form["new_status"]
        
        isUpdated = updateProfileController().updateUserProfile(rolename, new_rolename, new_description, new_status)

        if isUpdated:
            message = "User Profile Updated Successfully!"
            message_type = "success"
        else:
            message = "Failed - Role already exists"
            message_type = "error"
            return render_template('Admin/upUpdate.html', message=message, message_type=message_type, profile_info=profile_info)

    session.pop("profile_info=profile_info", None)
    return render_template('Admin/upUpdate.html', message=message, message_type=message_type)


#14 As a User Admin, I want to suspend user accounts so that I can revoke access to the system for users who are no longer available, ensuring they cannot log in or use their accounts anymore.
@admin_blueprint.route('/suspend_ua', methods=['GET', 'POST'])
def displaySuspendUserAccount():
    message = None

    if request.method == 'GET':
        user_info = session.get("user_info")
        return render_template('Admin/uaSuspend.html', user_info=user_info)
    
    elif request.method == "POST":
        user_info = session.get("user_info")
        username = user_info['username'] if user_info else None
        isSuspended = suspendAccountController().suspendUserAccount(username)

        if isSuspended:
            message = "User Account Suspended Successfully!"
            user_info['acc_status'] = 0  # Mark as inactive
            session["user_info"] = user_info 
    
    session.pop("user_info", None)
    return render_template('Admin/uaSuspend.html', message=message, user_info=user_info)


#15 As a User Admin, I want to suspend user profiles so that I can remove all associated personal information and user types from the system, even if the user’s account remains active.
@admin_blueprint.route('/suspend_up', methods=['GET', 'POST'])
def displaySuspendUserProfile():
    message = None

    if request.method == 'GET':
        profile_info = session.get("profile_info")
        return render_template('Admin/upSuspend.html', profile_info=profile_info)
    
    if request.method == "POST":
        profile_info = session.get("profile_info")
        role = profile_info['role'] if profile_info else None

        isSuspended = suspendProfileController().suspendUserProfile(role)

        if isSuspended:
            message = "User Profile Suspended Successfully!"
            profile_info['pf_status'] = 0 # Mark as inactive
            session["profile_info"] = profile_info
            
    session.pop("profile_info", None)  
    return render_template('Admin/upSuspend.html', message=message, profile_info=profile_info)


#16 As a User Admin, I want to search for the user account so that I can find the particular user account.
@admin_blueprint.route('/search_ua', methods=['GET', 'POST'])
def displaySearchUserAccount():
    if request.method == "POST":
        username = request.form["username"]
        user_info = searchAccountController().searchUserAccount(username)

        if user_info:
            session["user_info"] = user_info
            message = "User Account Found Successfully!"
            message_type = "success"
            return render_template('Admin/uaSearch.html', user_info=user_info, message=message, message_type=message_type)
        else:
            message = "User Account Not Found..."
            message_type = "error"
        return render_template('Admin/uaSearch.html', user_info=[], message=message, message_type=message_type)
    
    return render_template('Admin/uaSearch.html')


#17 As a User Admin, I want to search for the user profile so that I can find the particular user profile.
@admin_blueprint.route('/search_up', methods=['GET', 'POST'])
def displaySearchUserProfile():
    if request.method == "POST":
        role = request.form["role"]
        profile_info = searchProfileController().searchUserProfile(role)

        if profile_info:
            session["profile_info"] = profile_info
            message = "User Profile Found Successfully!"
            message_type = "success"
            return render_template('Admin/upSearch.html', profile_info=profile_info, message=message, message_type=message_type)
        else:
            message = "User Profile Not Found..."
            message_type = "error"
        return render_template('Admin/upSearch.html', profile_info=[], message=message, message_type=message_type)
    
    return render_template('Admin/upSearch.html')


    
