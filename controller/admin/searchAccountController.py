from entity.userAccount import userAccount

class searchAccountController():
    
    def searchUserAccount(self, username):
        return userAccount().searchUserAccount(username)