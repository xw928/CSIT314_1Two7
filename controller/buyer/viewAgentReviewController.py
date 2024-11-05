from entity.review import review

class viewAgentReviewController():

    def getAllAgentReview(self):
        return review().getAllAgentReview()