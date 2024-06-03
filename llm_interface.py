
class LLMInterface:
    def __init__(self, models):
        self.models = models
    
    def query_all(self, prompt):
        responses = {}
        for model in self.models:
            # Code to query the model
            responses[model] = "Response from " + model
        return responses
