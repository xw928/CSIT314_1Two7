from entity.userAccount import userAccount

class resetPasswordController():
    
    def resetUserPassword(self, username, new_password):
        return userAccount().resetUserPassword(username, new_password)

