# Prompt formatting operations
from typing import List, Dict, Protocol

class PromptFormatter(Protocol):
    """
    Prompt converter protocol for different model formats.
    """

    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Converts the message list to the format expected by the model.
        """

        pass

class GemmaPromptFormatter:
    """
    Prompt formatter for Gemma model.
    """

    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Converts message list to Gemma format.

        Args:
        messages: List of messages (vocabularies with roles and content)

        Returns:
        str: Prompt in Gemma format
        """
        formatted_prompt = ""
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "system":
                formatted_prompt += f"<s>[INST] <<SYS>>\n{content}\n<</SYS>>\n\n"

            elif role == "user":
                # If the previous message is not system, add a new [INST] tag.
                if not formatted_prompt.endswith("[INST] ") and not formatted_prompt.endswith("\n\n"):
                    formatted_prompt += f"[INST] {content} [/INST]\n"

                else:
                    formatted_prompt += f"{content} [/INST]\n"

            elif role == "assistant":
                formatted_prompt += f"{content}\n\n"

        return formatted_prompt.strip()


class ChatMLPromptFormatter:
    """
    Prompt formatter for models using ChatML format (GPT etc.).
    """

    def format_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Converts message list to ChatML format.
        """

        formatted_prompt = ""

        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")

            formatted_prompt += f"<|im_start|>{role}\n{content}<|im_end|>\n"

        # Last tag for the assistant response
        formatted_prompt += "<|im_start|>assistant\n"
        return formatted_prompt