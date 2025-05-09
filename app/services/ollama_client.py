# Communication with Ollama API
import httpx
from typing import Dict, Any, Tuple
from app.core.config import OLLAMA_URL, API_TIMEOUT

class OllamaClient:
    """
    The OllamaClient class is responsible for communicating with the Ollama API.
    """

    def __init__(self, base_url=OLLAMA_URL, timeout=API_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout

    async def generate(self, model_name: str, prompt: str, options: Dict[str, Any] = None) -> Tuple[bool, str]:
        """
        Sends a /api/generate request to the Ollama API.

        Args:
            model_name: Model name
            prompt: Request context (with text format)
            options: Extra options for the model (temperature etc.)

        Returns:
            Tuple[bool, str]: (Success situation, Response text)
        """

        if options is None:
            options = {"temperature": 0.7}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                print(f"Sending a request to Ollama: {self.base_url}/api/generate")
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": options
                    }
                )
                print(f"Ollama response situation: {response.status_code}")
                response.raise_for_status()
                data = response.json()
                return True, data.get('response', '')

        except httpx.ReadTimeout:
            print("Ollama timeout!")
            return False, "I am so sorry, but there is a timeout during the LLM response process. Try asking different question or contact with system administrator."
        except Exception as e:
            print(f"Error during the Ollama process: {str(e)}")
            return False, f"I am so sorry, an error happened: {str(e)}"