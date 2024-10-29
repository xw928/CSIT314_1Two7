from entity.userProfile import userProfile

class getAvailableRoleController():
    def getAvailableRole(self):
        return userProfile().getAvailableRole()