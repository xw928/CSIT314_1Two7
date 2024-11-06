from entity.buyerShortList import buyerShortList

class viewBuyerShortListedCarController():

    def viewShortListedCar(self, buyer_username):
        return buyerShortList().viewShortListedCar( buyer_username)