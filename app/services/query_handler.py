# Service managing user queries
from app.core.memory import memory_manager
from app.services.ai_service import AIService
from app.core.config import SYSTEM_PROMPT, USING_MODEL
from app.data.data_provider import get_data
from app.utils.compact_data_handler import CompactDataHandler
from app.data.data_creator import initialize_data

async def handle_query(question: str, access_token: str):
    # Use token information directly
    user_token = access_token
    api_data = await initialize_data(access_token)  # Get API data

    # Add the question to the memory
    memory_manager.add_message(user_token, "user", question)

    # Get last messages from the memory
    history = memory_manager.get_context(user_token)

    # Firstly, get the system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    # Give the user's question to the API
    messages.append({"role": "user", "content": f"{get_data()}\n\nQuestion: {question}"})

    # Start the AI engine
    ai_service = AIService(model_name=USING_MODEL)

    # Send the question to the AI and get the response
    response = await ai_service.ask(messages)

    # Add response to the memory
    memory_manager.add_message(user_token, "assistant", response)

    return {"response": response}

if __name__ == "__main__":
    print(get_data())
