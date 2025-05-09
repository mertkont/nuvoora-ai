# Assistant's temporary memory (context)
from collections import defaultdict, deque
from app.core.config import MESSAGE_MEMORY

class MemoryManager:
    def __init__(self, max_len=MESSAGE_MEMORY):
        self.memory = defaultdict(lambda: deque(maxlen=max_len))

    def add_message(self, user_token: str, role: str, content: str):
        """
        Add the message to the memory
        """
        self.memory[user_token].append({"role": role, "content": content})

    def get_context(self, user_token: str):
        """
        Return the past messages of the user as a list
        """
        return list(self.memory[user_token])

    def reset_memory(self, user_token: str):
        """
        Reset the memory of the user
        """
        self.memory[user_token].clear()

# Create a singleton
memory_manager = MemoryManager()