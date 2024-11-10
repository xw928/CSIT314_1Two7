from entity.buyerShortList import buyerShortList

class searchBuyerShortListController:
    
    def searchBuyerShortList(self, buyer_username, field, value):
        return buyerShortList().searchBuyerShortList(buyer_username, field, value)