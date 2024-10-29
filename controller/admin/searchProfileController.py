from entity.userProfile import userProfile

class searchProfileController():
    
    def searchUserProfile(self, role):
        return userProfile().searchUserProfile(role)