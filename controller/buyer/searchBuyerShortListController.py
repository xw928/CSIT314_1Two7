from entity.buyerShortList import buyerShortList

class searchBuyerShortListController:
    
    def searchBuyerShortList(self, field, value, buyer_username):
        return buyerShortList().searchBuyerShortList(field, value, buyer_username)