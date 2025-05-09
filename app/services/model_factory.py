# Model creation and management
# Create a model with the class added into ai_models
from app.core.ai_models import GemmaModel, GPTModel, GeminiModel

class ModelFactory:
    """
    Factory class for AI models
    """

    @staticmethod
    def create_model(model_name: str):
        """
        Returns suitable AI model class instance

        Args:
            model_name: Model type ("gemma3", "gpt", "gemini", etc.)

        Returns:
            AIModelInterface: Model class sample
        """
        model_name = model_name.lower()

        if model_name == "gemma3" or model_name.startswith("gemma"):
            return GemmaModel(model_name)

        elif model_name == "gpt" or model_name.startswith("gpt"):
            return GPTModel()

        elif model_name == "gemini" or model_name.startswith("gemini"):
            return GeminiModel()

        else:
            raise ValueError(f"Unknown model type: {model_name}")