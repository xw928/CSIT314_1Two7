from entity.userAccount import userAccount

class suspendAccountController():

    def suspendUserAccount(self, username):
        return userAccount().suspendUserAccount(username)