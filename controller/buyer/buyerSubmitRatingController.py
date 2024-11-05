from entity.rating import rating

class buyerSubmitRatingController():

    def submitRating(self, agent_username, sender_username, buyer_rating):
        return rating().submitRating(agent_username, sender_username, buyer_rating)