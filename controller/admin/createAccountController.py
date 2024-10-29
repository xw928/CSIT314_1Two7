from entity.userAccount import userAccount

class createAccountController():

    def createUserAccount(self, username, password, profile_id):
        return userAccount().createUserAccount(username, password, profile_id)