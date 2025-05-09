# Ollama service status and helper functions
import httpx
from app.core.config import OLLAMA_URL

async def check_ollama_service():
    """
    Checks whether the ollama service is reachable.

    Returns:
        tuple: (success (bool), message (str))
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check if ollama service is running
            response = await client.get(f"{OLLAMA_URL}")

            if response.status_code == 200:
                return True, "Ollama service is working."

            else:
                return False, f"Ollama service answered, but the status code: {response.status_code}"

    except httpx.ConnectError:
        return False, f"Cannot connect to the Ollama service. Make sure to the Ollama process is working on that URL: {OLLAMA_URL}."

    except httpx.ReadTimeout:
        return False, "Ollama service is timeout."

    except Exception as e:
        return False, f"An error occurred during to the controlling process of the Ollama process: {str(e)}"

async def list_models():
    """
    Lists models available in Ollama.

    Returns:
        tuple: (success (bool), models (list) or error_message (str))
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = [model.get("name") for model in data.get("models", [])]
                return True, models

            else:
                return False, f"Cannot get models. Status code: {response.status_code}"

    except Exception as e:
        return False, f"An error occured during to the listing process of models: {str(e)}"