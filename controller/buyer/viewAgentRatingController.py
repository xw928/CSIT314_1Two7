from entity.rating import rating

class viewAgentRatingController():

    def getAllAgentRating(self):
        return rating().getAllAgentRating()