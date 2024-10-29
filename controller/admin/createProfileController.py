from entity.userProfile import userProfile

class createProfileController():

    def createUserProfile(self, role, description):
        return userProfile().createUserProfile(role, description)