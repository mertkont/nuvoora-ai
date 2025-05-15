# AI model implementations
# We can add a class here to add a new model
from typing import List, Dict
from app.core.interfaces import AIModelInterface
from app.services.ollama_client import OllamaClient
from app.utils.prompt_formatter import GemmaPromptFormatter, ChatMLPromptFormatter
from app.core.config import API_KEY
import google.generativeai as genai

class GemmaModel(AIModelInterface):
    """
    Implementations for Gemma model
    """

    def __init__(self, model_name="gemma3"):
        self.model_name = model_name
        self.client = OllamaClient()
        self.formatter = GemmaPromptFormatter()

    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Sends messages to Gemma model and returns response

        Args:
            messages: Message list

        Returns:
            str: Model response
        """
        # Transform messages into Gemma format
        formatted_prompt = self.formatter.format_messages(messages)

        # Send a request on Ollama client
        success, response = await self.client.generate(
            model_name=self.model_name,
            prompt=formatted_prompt
        )

        if not success:
            return f"Error: {response}"

        return response


class GPTModel(AIModelInterface):
    """
    Implementation for OpenAI GPT models
    """

    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name
        self.formatter = ChatMLPromptFormatter()

    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Sends messages to OpenAI GPT model and returns response

        Args:
            messages: Message list

        Returns:
            str: Model response
        """
        import openai

        try:
            client = openai.AsyncOpenAI(api_key=API_KEY)
            # OpenAI accepts this response type
            response = await client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"GPT model error: {str(e)}"


class GeminiModel(AIModelInterface):
    """
    Implementation for Google Gemini model
    """

    def __init__(self, model_name="gemini-2.0-flash-001"):
        self.model_name = model_name
        self.formatter = ChatMLPromptFormatter()
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(model_name=self.model_name)

    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Sends messages to Gemini model and returns response

        Args:
            messages: Message list

        Returns:
            str: Model response
        """
        try:
            formatted_prompt = self.formatter.format_messages(messages)

            # Gemini model generally works on a prompt basis, but it may also support a "chat" method.
            response = await self.model.generate_content_async(formatted_prompt)

            return response.text
        except Exception as e:
            return f"Gemini model error: {str(e)}"
