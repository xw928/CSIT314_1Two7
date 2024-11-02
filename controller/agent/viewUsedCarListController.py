from entity.usedCarList import usedCarList

class viewUsedCarListController():

    def viewUsedCarList(self, agent_username):
        return usedCarList().viewUsedCarList(agent_username)