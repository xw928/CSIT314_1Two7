from entity.rating import rating

class sellerSubmitRatingController():

    def submitRating(self, agent_username, sender_username, seller_rating):
        return rating().submitRating(agent_username, sender_username, seller_rating)