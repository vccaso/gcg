from abc import ABC, abstractmethod


class ModelBase(ABC):

    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        

    @abstractmethod
    def get_response(self, prompt):
        """
        Uses a model to ask a question. Returns the model response.
        """
        pass