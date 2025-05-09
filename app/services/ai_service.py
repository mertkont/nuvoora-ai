# High-level AI business logic
from typing import List, Dict
from app.services.model_factory import ModelFactory
from app.core.config import USING_MODEL

class AIService:
    """
    AI service - high level API
    """
    def __init__(self, model_name=USING_MODEL):
        self.model_name = model_name
        self.model = ModelFactory.create_model(model_name)

    async def ask(self, messages: List[Dict[str, str]]) -> str:
        """
        Asks a question and gets a response from the AI model.

        Args:
            messages: Message list

        Returns:
            str: Model yanıtı
        """
        return await self.model.generate_response(messages)

    def change_model(self, model_name: str):
        """
        Changes used model

        Args:
            model_name: New model name
        """
        self.model_name = model_name
        self.model = ModelFactory.create_model(model_name)