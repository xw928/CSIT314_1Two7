from entity.userProfile import userProfile

class suspendProfileController():

    def suspendUserProfile(self, role):
        return userProfile().suspendUserProfile(role)