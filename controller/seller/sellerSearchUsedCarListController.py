from entity.usedCarList import usedCarList

class sellerSearchUsedCarListController():

    def sellerSearchUsedCarList(self, seller_username, field, value):
        return usedCarList().searchSellerUsedCarList(seller_username, field, value)