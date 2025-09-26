# app/chat.py

from app.api_client import GroqClient
from logger import CustomLogger

class ChatManager:
    """Class to manage chat interactions."""

    def __init__(self):
        self.client = GroqClient()  
        self.conversation_history = []  
        self.logger = CustomLogger().get_logger()

    def add_message(self, role, content):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_response(self, user_message):
        """
        Get a response based on user input and maintain conversation history.

        :param user_message: The message input from the user.
        :return: AI response as a string.
        """
        user_message = user_message.strip()
        if not user_message:
            return "Please enter a message."

        self.add_message("user", user_message)
        self.logger.info(f"User: {user_message}")

        if any(keyword in user_message.lower() for keyword in ["what is", "define"]):
            prompt = f"Provide a concise definition of: {user_message}"
        elif "explain" in user_message.lower() or "code" in user_message.lower():
            prompt = f"Explain clearly with examples: {user_message}"
        else:
            prompt = f"Respond concisely to: {user_message}"

        temp_history = self.conversation_history.copy()
        temp_history.append({"role": "user", "content": prompt})

        ai_response = self.client.get_response(temp_history)

        self.add_message("assistant", ai_response)
        self.logger.info(f"Assistant: {ai_response}")

        return ai_response
