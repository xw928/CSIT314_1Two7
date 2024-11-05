from entity.usedCarList import usedCarList

class sellerViewUsedCarListController():

    def viewUsedCarList(self, seller_username):
        return usedCarList().viewUsedCarList(seller_username)