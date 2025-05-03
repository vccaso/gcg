# agents/validator_base.py
from abc import ABC, abstractmethod

class ValidatorBaseAgent(ABC):
    @abstractmethod
    def validate(self, input_data: dict) -> dict:
        """
        Validates the result of another agent.
        Returns a dict with 'status' (pass/fail) and optional 'reason'.
        """
        pass
