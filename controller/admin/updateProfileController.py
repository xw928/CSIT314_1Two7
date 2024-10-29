from entity.userProfile import userProfile

class updateProfileController():
    
    def updateUserProfile(self, rolename, new_rolename, new_description, new_status):
    
        return userProfile().updateUserProfile(rolename, new_rolename, new_description, new_status)

