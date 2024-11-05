from entity.usedCarList import usedCarList

class searchUsedCarListController():
    
    def searchBuyerUsedCarList(self, buyer_username, field, value):
        return usedCarList().searchBuyerUsedCarList(buyer_username, field, value)