from entity.review import review

class sellerSubmitReviewController():

    def submitReview(self, agent_username, sender_username, seller_review):
        return review().submitReview(agent_username, sender_username, seller_review)