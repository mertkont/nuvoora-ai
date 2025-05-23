# Definition of AI model interfaces
from abc import ABC, abstractmethod
from typing import List, Dict

class AIModelInterface(ABC):
    """
    Interface that AI models must comply with.

    New model types must implement this interface.
    """

    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generates a response based on the given messages.

        Args:
        messages: List of messages (dictionaries containing roles and content)

        Returns:
        str: Response generated by the model
        """

        pass