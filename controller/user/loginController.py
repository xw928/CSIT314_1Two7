from entity.userAccount import userAccount

class loginController():

    def verifyAccount(self, username, password):
        return userAccount().verifyAccount(username, password)
