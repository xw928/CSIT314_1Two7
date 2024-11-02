from entity.usedCarList import usedCarList

class searchUsedCarListController():
    
    def searchUsedCarList(self, agent_username, field, value):
        return usedCarList().searchUsedCarList(agent_username, field, value)