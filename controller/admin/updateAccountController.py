from entity.userAccount import userAccount

class updateAccountController():
    
    def updateUserAccount(self, username, new_username, new_password, new_role, new_status):
    
        return userAccount().updateUserAccount(username, new_username, new_password, new_role, new_status)

