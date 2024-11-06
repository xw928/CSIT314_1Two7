from entity.buyerShortList import buyerShortList

class addToBuyerShortListController():

    def addBuyerShortList(self, buyer_username, car_id):
        return buyerShortList().addBuyerShortList( buyer_username, car_id)